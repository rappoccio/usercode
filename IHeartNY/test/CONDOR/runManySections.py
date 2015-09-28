#! /usr/bin/env python

import optparse
import re
import os
import sys
import commands
import tempfile
import time
from xml.dom  import minidom
from pprint   import pprint
from glob     import glob
from datetime import datetime

############################################
## ###################################### ##
## ## Global Information and Functions ## ##
## ###################################### ##
############################################

# global REs
commentRE      = re.compile (r'#.+$')
firstLogRE     = re.compile (r'^\s*(\S+)\s+(\S.+$)')
varDefRE       = re.compile (r'^-\s*(\w+)\s*=\s*(\S.*)')
emptyVarDefRE  = re.compile (r'^-\s*(\w+)\s*=\s*$')
dashRE         = re.compile (r'^-')
leadingSlashRE = re.compile (r'^/')
dotSlashRE     = re.compile (r'^\./')
logRE          = re.compile (r'\.log$', re.IGNORECASE)
envRE          = re.compile (r'\$\((\w+)\)')
stringNumRE    = re.compile (r'\$(\d+)')
loadRE         = re.compile (r'inputFiles_load=(\S+)')

# bash name
bashname = 'runMany.bash'

# section info
sectionInfo = "section=%d totalSections=%d"

# condor output directory
condorOutputDir = 'notneeded'

# log suffix
logSuffix = '.log'

# condor command file
condor = '''universe = vanilla
Executable            = %(command)s
Requirements          = Memory >= 199 &&OpSys == "LINUX"&& (Arch != "DUMMY" )&& Disk > 1000000
Should_Transfer_Files = YES
WhenToTransferOutput  = ON_EXIT_OR_EVICT
Output = %(condorOutputDir)s/candelete_$(Cluster)_$(Process).stdout
Error  = %(condorOutputDir)s/candelete_$(Cluster)_$(Process).stderr
Log    = %(condorOutputDir)s/candelete_$(Cluster)_$(Process).log
Notification    = Error
notify_user     = %(user)s@FNAL.GOV
Arguments       = %(arguments)s
%(extraLines)s
Queue %(numSections)s\n'''

# CMSSW variables
cmsswFNALbashrc = '/uscmst1/prod/sw/cms/bashrc'
cmsswEnvFNAL = 'cd %%s; . %s prod; eval `scramv1 runtime -sh`; cd -' % cmsswFNALbashrc

cmsswEnvCERN = 'cd %s; eval `scramv1 runtime -sh`; cd -'

storageXml = '$(CMS_PATH)/SITECONF/local/PhEDEx/storage.xml'
storageProtocals = ['dcap']

def loadStorageXml ():
    ''' '''
    fullStorageXml = expandEnvironmentVariables (storageXml)
    retval = []
    try:
        source = open (fullStorageXml, 'r')
    except:
        # nothing to see here
        return retval
    xmldoc = minidom.parse(source).documentElement
    source.close()
    for piece in xmldoc.getElementsByTagName('lfn-to-pfn'):
        if piece.getAttribute('protocol') not in storageProtocals:
            continue
        first = piece.getAttribute('path-match')
        pathMatch = stringNumRE.sub (r'\\\1', str(first))
        targetString = stringNumRE.sub (r'\\\1',
                                        piece.getAttribute('result') )
        retval.append( ( re.compile (pathMatch), targetString) )
        #print "pm", pathMatch, "ts", targetString
    return retval


def convertLfn2Pfn (lfnList, pfnList):
    '''Converts a list of files from Lfn to Pfn'''
    storageList = loadStorageXml()
    try:
        source = open (lfnList, 'r')
    except:
        raise RuntimeError, "Can't open '%s' for reading." % lfnList
    try:
        target = open (pfnList, 'w')
    except:
        raise RuntimeError, "Can't open '%s' for writing." % pfnList
    for line in source:
        line = line.strip()
        for (regex, replace) in storageList:
            newline = regex.sub (replace, line)
            if newline != line:
                line = newline
                break
        target.write ('%s\n' % line)
    source.close()
    target.close()
        

def absPath (filename, withoutFilename = False):
    '''Returns the full absolute path to a given file'''
    dirname  = os.path.dirname  (filename)
    basename = os.path.basename (filename)
    if leadingSlashRE.match (dirname):
        # we have a full path
        if withoutFilename:
            return dirname
        else:
            return "%s/%s" % (dirname, basename)
    # if we're here, we have a relative path
   # first get rid of a leadint './'
    dirname = dotSlashRE.sub ('', dirname)
    if dirname == '.':
        dirname = '' 
    if dirname:
        if withoutFilename:
            return "%s/%s" % (os.getcwd(), dirname)
        else:
            return "%s/%s/%s" % (os.getcwd(), dirname, basename)
    else:
        if withoutFilename:
            return os.getcwd()
        else:
            return "%s/%s" % (os.getcwd(), basename)


def _replEnvVar (match):
    return os.environ.get (match.group(1),'$(%s)' % match.group(1))


def expandEnvironmentVariables (variable):
    '''Replaces environment variables with their values'''
    retval = envRE.sub (_replEnvVar, variable)
    return retval


def epochTimeInHex():
    '''Returns current time as epoch time in hex'''
    now = datetime.now()
    return hex( int( time.mktime( now.timetuple() ) ) )[2:]

    
#############################
## ####################### ##
## ## SectionInfo Class ## ##
## ####################### ##
#############################

class SectionInfo (object):
    '''Object designed to hold necessary information about different
    Sections'''

    allowed = []
    clusterValue = None
    first        = True

    def __init__ (self, command, firstIsLog = True, **kwargs):
        self.index = -1
        if firstIsLog:
            match = firstLogRE.match (command)
            if not match:
                raise RuntimeError, "Command '%s' is mailformed" % command
            self._log     = match.group(1)
            self._command = match.group(2)
        else:
            self._log = 'output_$(JID).log'
            self._command = command            
        # if there's anything else to set, let's make sure we're
        # supposed to first:
        for key, value in kwargs.iteritems():
            key = key.lower()
            if key in SectionInfo.allowed:
                setattr (self, key, value)
            else:
                # not allowed to set this here
                raise RuntimeError, "Illegal key '%s'." % key
        # remove .log name
        self._log = logRE.sub ('', self._log)

    def __str__ (self):
        return "%-20s %s" % (self._log, self._command)

    def _setupProcess (self):
        '''If asked, it sets up necessary environment variables to
        duplicate names generated in batch jobs.'''
        if SectionInfo.first:
            SectionInfo.first = False
            if SectionInfo.clusterValue:
                os.environ['Cluster'] = SectionInfo.clusterValue
        if SectionInfo.clusterValue:
            os.environ['Process'] = '%d' % self.index
            os.environ['JID'] = 'JID_%d_%d' % (SectionInfo.clusterValue,
                                               self.index)

    def log (self, expand = True):
        retval = self._log
        if expand:
            self._setupProcess()
            retval =  expandEnvironmentVariables (retval)
        return retval


    def command (self, expand = True):
        retval = self._command
        if expand:
            self._setupProcess()
            retval =  expandEnvironmentVariables (retval)
        return retval


#######################################
## ################################# ##
## ## SectionInfoCollection Class ## ##
## ################################# ##
#######################################

class SectionInfoCollection (object):
    '''Object designed to hold many SectionInfo objects'''

    allowed = ['env', 'tag', 'output', 'extraoptions', 'outputsuffix',
               'tagmode', 'tarfile', 'untardir', 'copycommand']

    allowedValues = { 'tagmode' : ('atend', 'none') }

    def __init__ (self):
        self.output      = 'outputFile='
        self.env         = 'echo Nothing setup for environment'
        self.siList      = []
        self.tag         = ''
        self.tagmode     = 'none'
        self.tarfile     = ''
        self.untardir    = 'tardir'
        self.copycommand = 'cp'


    def __len__ (self):
        return len (self.siList)


    def __str__ (self):
        retval = '# variable definitions\n'
        for varname in SectionInfoCollection.allowed:
            try:
                value = getattr (self, varname)
                retval += '- %s = %s\n' % (varname, value)
            except:
                pass
        retval += '\n# Sections listed\n'
        retval += self.sectionsListedOnly()
        ## retval += "size %d\n" % len (self.siList)
        ## for index, bla in enumerate (self.siList):
        ##     retval += "  %d) %s\n" % (index, bla)
        ## retval += "%s" % self.siList
        return retval


    def __getitem__ (self, index):
        if not isinstance (index, int):
            raise RuntimeError, "Index '%s' must be an integer" % index
        return self.siList[index]


    def _validateVariables (self):
        '''Validates that variables passed by control file are all set
        appropriately.'''
        for key, tup in SectionInfoCollection.allowedValues.iteritems():
            try:
                value = getattr (self, key)
            except:
                continue
            if value not in tup:
                raise RuntimeError, "Variable '%s' has illegal value '%s'. Allowed values are %s." % (key, value, tup)


    def sectionsListedOnly (self):
        '''Returns a string of the sections listed without anything
        else'''
        retval = ''
        for si in self.siList:
            retval += "%s\n" % si
        return retval


    def readControlFile (self, filename, firstIsLog = True):
        '''Reads in information from control file.  Returns list with
        necessary information.'''
        try:
            source = open (filename, 'r')
        except:
            raise RuntimeError, "File '%s' not found." % filename
        for line in source:
            # get rid of comments and blank lines
            line = commentRE.sub ('', line)
            line = line.strip()
            if not line:
                continue
            # is this a variable definition?
            match = varDefRE.match (line)
            if match:
                var   = match.group(1).lower()
                value = match.group(2)
                if var not in SectionInfoCollection.allowed:
                    raise RuntimeError, "Variable definition error: '%s' unknown variable" % var
                setattr (self, var, value)
                continue
            # is this an empty variable definition
            match = emptyVarDefRE.match (line)
            if match:
                var   = match.group(1).lower()
                value = ''
                if var not in SectionInfoCollection.allowed:
                    raise RuntimeError, "Variable definition error: '%s' unknown variable" % var
                setattr (self, var, value)
                continue
            if dashRE.match (line):
                raise RuntimeError, "Can not parse line '%s' of configuration file '%s'." % (line, filename)
            # if we're still here, then treat the line as a SectionInfo
            info = SectionInfo (line, firstIsLog)
            info.index = len (self)
            self.siList.append( info )
        source.close()
        self._validateVariables()


    def cmsswEnv (self):
        '''Sets up current CMSSW release'''
        base = os.environ.get ('CMSSW_BASE', '')
        if not base:
            raise RuntimeError, "No version of CMSSW is setup"
        if os.path.exists (cmsswFNALbashrc):
            self.env = cmsswEnvFNAL % base
        else:
            self.env = cmsswEnvCERN % base


    def bashname (self):
        '''Assuming bash script is in same directory as this script,
        will return full path name to bash script.'''
        return "%s/%s" % (absPath (sys.argv[0], True), bashname)


    def log (self, index):
        '''Returns log name for given index'''
        return "%s%s" % (self[index].log(), logSuffix)


    def command (self, index, **options):
        '''Returns command name for given index'''
        retval = self[index].command()
        if options.has_key ('replaceFilelist'):
            match = loadRE.search (retval)
            if match:
                try:
                    os.mkdir ('temp')
                except:
                    pass
                oldList = match.group(1)
                newList = 'temp/newlist'
                convertLfn2Pfn (oldList, newList)
                retval = loadRE.sub ('inputFiles_load=%s' % newList, retval)
        if self.tagmode == 'atend':
            tag = self.tag
            if len (tag):
                tag += '_'
            tag += 'jid$(Cluster)_$(Process)'
            retval += ' tag=%s' % tag
        return expandEnvironmentVariables (retval)


    def fullCopyCommand (self, dest):
        '''returns full copy command which lists every file that is in
        the current directory that is itself not a directory and
        copies them to "dest".'''
        filesToCopy = " ".join( filter (os.path.isfile, glob ('*')) )
        return "%s %s %s" % (self.copycommand, filesToCopy, dest)


########################
## ################## ##
## ## Main Program ## ##
## ################## ##
########################

if __name__ =='__main__':


    ##################
    ## Setup Parser ##
    ##################
    parser = optparse.OptionParser ("Usage: %prog [options] commands.txt [index]")
    queueGroup = optparse.OptionGroup (parser, "QUEUE Options (used by 'runMany.bash')")
    appendGroup   = optparse.OptionGroup (parser, "Append Options")
    createGroup   = optparse.OptionGroup (parser, "Create Options")
    condorGroup   = optparse.OptionGroup (parser, "Condor Submit Options")
    lsfGroup      = optparse.OptionGroup (parser, "LSF Submit Options")
    testGroup     = optparse.OptionGroup (parser, "Test Options")
    validateGroup = optparse.OptionGroup (parser, "Validate Options (NOT YET IMPLEMNENTED)")
    debugGroup    = optparse.OptionGroup (parser, "Debugging Options (not for general use)")
    # QUEUE options
    queueGroup.add_option ('--env', dest='env', 
                           action="store_true",
                           help='print command necessary to setup environment')
    queueGroup.add_option ('--command', dest='command',  
                           action="store_true",
                           help='print out command of nth section')
    queueGroup.add_option ('--log', dest='log', 
                           action="store_true",
                           help='print out log of nth section')
    queueGroup.add_option ('--tarball', dest='tarball', 
                           action="store_true",
                           help='returns name of tarball, if any')    
    queueGroup.add_option ('--untardir', dest='untardir', 
                           action="store_true",
                           help='returns name of directory to untar tarball, if any')    
    queueGroup.add_option ('--replaceFilelist', dest='replaceFilelist', 
                           action="store_true",
                           help="use 'storage.xml' to correct filenames")
    queueGroup.add_option ('--copyCommand', dest='copyCommand', type='string',
                           metavar='DEST',
                           help='copy command to copy files back from queue to DEST')
    # append options
    appendGroup.add_option ('--appendToCommandFile', dest='appendTo',
                           action='store_true',
                           help='append to a command file given list of input files')
    appendGroup.add_option ('--numberPerSection', dest='numberPer', type='int',
                           default=1,
                           help='number of files to run on per section (default %default)')
    appendGroup.add_option ('--toUse', dest='toUse', type='string',
                           help='command to use to put together command file')
    appendGroup.add_option ('--logBase', dest='logBase', type='string',
                           default='log',
                           help='logfile base name (default %default)')
    # create options
    createGroup.add_option ('--createCommandFile', dest='create',
                            action='store_true',
                            help='create full command file given list of commands')
    createGroup.add_option ('--addLog', dest='addLog',
                            action='store_true', default=False,
                            help='assume lists of commands does not include a logfile name.  Creates default logfile name')
    createGroup.add_option ('--cmssw', dest='cmssw', 
                            action="store_true",
                            help='Use current CMSSW release for environment')
    createGroup.add_option ('--envString', dest='envString', type='string',
                            help='String to eval to setup environment')
    createGroup.add_option ('--setTarball', dest='setTarball', type='string',
                            help='set tarball filename to be sent to condor')
    createGroup.add_option ('--noUntarDir', dest='noUntarDir', 
                            action="store_true",
                            help="Untar tarball in main working directory instead of 'tardir/'")
    # condor options
    condorGroup.add_option ('--submitCondor', dest='submitCondor', 
                            action="store_true",
                            help='submit jobs to Condor queue')    
    condorGroup.add_option ('--dontSubmitCondor', dest='dontSubmitCondor', 
                            action="store_true",
                            help='pretend to submit jobs to Condor queue')    
    condorGroup.add_option ('--noDeleteCondor', dest='noDelete', 
                            action="store_true",
                            help='do not delete temporary condor file')    
    # lsf options
    lsfGroup.add_option ('--submitLsf', dest='submitLsf', 
                          action="store_true",
                          help='submit jobs to Lsf queue')
    lsfGroup.add_option ('--lsfOptions', dest='lsfOptions', type='string',
                          default='',
                          help='options to be passed to lsf command')
    lsfGroup.add_option ('--noLsfCopy', dest='noLsfCopy', 
                          action="store_true",
                          help='do not copy results results back from')
    # validate options
    validateGroup.add_option ('--validateLogs', dest='validateLogs', 
                              action="store_true",
                              help='validate jobs successfully run via log files')
    validateGroup.add_option ("--validateString", dest="validateString",
                              type="string",                   
                              help="defines string to be found to validate log (default: log file simply exists)")
    validateGroup.add_option ('--clusterID', dest='cluster', type='string',
                              help='cluster ID (jobid) value')
    # debug options
    debugGroup.add_option ('--testSection', dest='testSection', type='int',
                           default=-1,
                           help='number of files to run on per section (default %default)')
    debugGroup.add_option ('--runTest', dest='runTest', action='store_true',
                           help='runs test specified in --testSection')
    debugGroup.add_option ('--print', dest='printSelf', 
                           action="store_true",
                           help='Print out configuration file contents and then exits')
    debugGroup.add_option ('--internalTest', dest='internalTest', 
                           action="store_true",
                           help='For development only')
    # add in the groups and get the answer
    parser.add_option_group (queueGroup)
    parser.add_option_group (appendGroup)
    parser.add_option_group (createGroup)
    parser.add_option_group (condorGroup)
    parser.add_option_group (lsfGroup)
    parser.add_option_group (validateGroup)
    parser.add_option_group (debugGroup)
    (options, args) = parser.parse_args()

    # preprocessing
    if options.cluster:
        SectionInfo.clusterValue = options.cluster

    # start doing what was asked
    if len (args) < 1:
        raise RuntimeError, "Must provide exactly one file"
    commandsFile = args[0]
    collection = SectionInfoCollection()

    #############################################
    ## Appending Commands to Base Command File ##
    #############################################
    # must do before reading in control file
    if options.appendTo:
        if len (args) < 2:
            raise RuntimeError, "Must provide exactly one input file and one output file"
        collection.readControlFile (commandsFile, firstIsLog = False)
        length = len (collection)
        numSections = length / options.numberPer
        if length % options.numberPer:
            numSections += 1
        appendFile = args[1]
        alreadyExists = False
        if os.path.isfile (appendFile):
            alreadyExists = True
        inputList = absPath (commandsFile)
        try:
            target = open (appendFile, 'a')
        except:
            raise RuntimeError, "Can not open '%s' to append to." % appendFile
        # if this file doesn't
        if not alreadyExists:
            target.write ('# -*- sh -*- # for font lock mode\n')            
        for loop in range (1, numSections + 1):
            target.write ("%s%03d_jid$(Cluster)_$(Process)  %s  " %\
                          (options.logBase, loop, options.toUse))
            target.write ("inputFiles_load=%s  " % inputList)
            target.write (sectionInfo % (loop, numSections))
            target.write ('\n')
        target.close()
        sys.exit()        

    ##########################
    ##        Testing       ##
    ## (For Debugging Only) ##
    ##########################
    if options.internalTest:
        print collection.bashname()
        print "sub", stringNumRE.sub (r'\\\1', u'dcap://cmsdca.fnal.gov:24137/pnfs/fnal.gov/usr/cms/WAX/11/store/$1')
        print expandEnvironmentVariables ('one_$(Cluster)_three')
        loadStorageXml()
        convertLfn2Pfn (commandsFile)
        sys.exit()


    #######################################
    ## ################################# ##
    ## ## Here We Go:                 ## ##
    ## ## Load the Configuration File ## ##
    ## ## And Let's Go Play!          ## ##
    ## ################################# ##
    #######################################
    firstIsLog = not options.addLog 
    collection.readControlFile (commandsFile, firstIsLog=firstIsLog)

    ###########################################
    ## Printing Configuration File To stdout ##
    ###########################################
    if options.printSelf:
        print "%s" % collection
        sys.exit()

    #################
    ## Environment ##
    #################
    if (options.cmssw or options.envString or options.setTarball or
        options.noUntarDir) and not options.create:
        raise RuntimeError, "You can only use options in the 'Create' group when using '--createCommandfile'"
    if options.setTarball:
        if not os.path.exists (options.setTarball):
            raise RuntimeError, "Tarball '%s' does not exist." % options.setTarball
        collection.tarfile = absPath (options.setTarball)
        if not options.noUntarDir:
            collection.untardir = 'tardir'
    # Tell configuration file how to setup the environment
    if options.cmssw and options.envString:
        raise RuntimeError, "You can not setup both CMSSW and your own custom environment.  Do not use --cmssw and --envString options together."
    if options.cmssw:
        collection.cmsswEnv()
    if options.envString:
        collection.env = options.envString

    #########################
    ## Create Command File ##
    #########################
    if options.create:
        if len (args) < 2:
            raise RuntimeError, "Must provide exactly one input file and one output file"
        outputFile = args[1]
        try:
            target = open (outputFile, 'w')
        except:
            raise RuntimeError, "Can't open '%s' for writing." % outputFile
        target.write ('# -*- sh -*- # for font lock mode\n')
        target.write ('%s\n' % collection)
        target.close()
        # if we are not submitting this job, then we are done
        if not options.submitCondor and not options.dontSubmitCondor:
            sys.exit()
        # If we're still here, make the file that is written above be
        # the commands file
        commandsFile = outputFile

    #################################
    ## Submit Jobs to Condor Queue ##
    #################################
    if options.submitCondor or options.dontSubmitCondor:
        extraLines = ''
        if collection.tarfile:
            extraLines += 'transfer_input_files = %s\n' % collection.tarfile
        argDict = \
                { 'command'     : collection.bashname(),
                  'user'        : commands.getoutput ('whoami'),
                  'arguments'   : '%s %s $(Process) $(Cluster)' \
                  % (absPath (sys.argv[0], True),
                     absPath (commandsFile)),
                  'numSections' : len (collection),
                  'extraLines'  : extraLines,
                  'condorOutputDir' : condorOutputDir
                  }
        try:
            tempTuple = tempfile.mkstemp (dir='.', prefix='condor-')
            name   = tempTuple[1]
            target = os.fdopen (tempTuple[0]  , "w+b")
        except:
            raise RuntimeError, "Failed to open temporary file"
        print "condor file:", name
        target.write (condor % argDict)
        target.close()
        try:
            os.mkdir (condorOutputDir)
        except:
            pass
        if options.submitCondor:
            os.system ('condor_submit %s' % name)
        if not options.noDelete:
            os.unlink (name)
        sys.exit()

    ############################
    ## Submit Jobs Via 'lsf' ##
    ############################
    if options.submitLsf:
        base = 'bsub %s %s %s %s' % \
               (options.lsfOptions,
                collection.bashname(),
                absPath (sys.argv[0], True),
                absPath (commandsFile))
        print "base", base
        cluster = epochTimeInHex()
        pwd = os.getcwd()
        if options.noLsfCopy:
            pwd = ''
        for process in range( len (collection) ):
            command = '%s %s %s %s' % (base, process, cluster, pwd)
            print command
            os.system (command)
        sys.exit()

    ###########################
    ## Bash Access Functions ##
    ###########################
    if options.command or options.log:
        if len (args) < 2:
            raise RuntimeError, "Must provide exactly one file and an index"
        try:
            index = int (args[1])
        except:
            raise RuntimeError, "Index '%s' must be an integer" % args[1]

    if options.copyCommand:
        print collection.fullCopyCommand (options.copyCommand)
        sys.exit()
    # print env
    if options.env:
        print collection.env
        sys.exit()
    # print tarball and untardir
    if options.tarball:
        baseTarfile = os.path.basename( collection.tarfile )
        if os.path.exists (baseTarfile):
            print baseTarfile
        else:
            print collection.tarfile
        sys.exit()
    if options.untardir:
        print collection.untardir
        sys.exit()

    # print command
    if options.command:
        print collection.command (index, **options.__dict__)
        sys.exit()
    # print log
    if options.log:
        print collection.log (index)
        sys.exit()

    if options.testSection >= 0:
        command = "%s %s %s %d 123" % \
                  (collection.bashname(),
                   absPath (sys.argv[0], True),
                   absPath (commandsFile),
                   options.testSection)
        print command
        if options.runTest:
            os.system (command)
        sys.exit()
        
    # if we're here then we have no idea what to do
    print "No options given."
    parser.print_help()
