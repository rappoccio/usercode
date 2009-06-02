#!/usr/bin/perl

# The input record separator is defined by Perl global
# variable $/.  It can be anything, including multiple
# characters.  Normally it is "\n", newline.  Here, we
# say there is no record separator, so the whole file
# is read as one long record, newlines included.
undef $/;

# get the inputs
$crab=$ARGV[0];
$cmssw=$ARGV[1];
$dataset=$ARGV[2];
$outdir=$ARGV[3];
$outfile=$ARGV[4];
$number=$ARGV[5];

print "---------------------\n";
print "usage: ./my_multicrab.pl crab.cfg cmssw.py /my/dataset /my/outdir myoutfile.root number\n";

print "Using $crab as a template\n";
print "Changing:\n";
print "cmssw python file = $cmssw \n";
print "dataset           = $dataset \n";
print "outdir            = $outdir \n";
print "outfile           = $outfile \n";
print "number of events  = $number \n";

# open the file
if (! open(INPUT,"<$crab") ) {
  print STDERR "Can't open file $crab\n";
  exit(0);
}

# slurp it in as one long record
$data = <INPUT>;
close INPUT;

# do the substitutions
$data =~ s/DUMMY_CMSSW/$cmssw/g;
$data =~ s/DUMMY_DATASET/$dataset/g;
$data =~ s/DUMMY_FILE/$outfile/g;
$data =~ s/DUMMY_OUTDIR/$outdir/g;
$data =~ s/DUMMY_NUMBER/$number/g;

# rename the output file
$outname = $crab;
$outname =~ s/dummy/$outdir/g;

print "Printing to $outname\n";

# open the output file
if (! open(OUTPUT, ">$outname") ) {
  die "Can't open output file $outname\n";
}

#print "Data is :\n";
#print $data;
#print "\n";

# print out the output
print OUTPUT $data;
close OUTPUT;
print STDERR "$outname was written\n";

print "Executing : crab -create -cfg $outname \n";
system "crab -create -cfg $outname \n";
print "Executing : crab -submit -cfg $outname \n";
system "crab -submit \n";

exit(0);
