/////////////////////////////////
// Class to study the semileptonic decay of ~g->~t_1 decay:
// It stores the P4 of the decay products
//
////////////////////////////////
#include <memory>
#include "Analysis/EDSHyFT/plugins/BoostedSusy.h"

using namespace std;
using namespace edm;
using namespace reco;

void BoostedSusy::produce(edm::Event& event, const edm::EventSetup& setup)
{

   //~g -> ~t_1 t, ~t_1 -> chi0 t
   //=============================
   // Stop products
   // ---------------
   std::auto_ptr< LorentzV > chi0G1   ( new LorentzV() );
   std::auto_ptr< LorentzV > chi0G2   ( new LorentzV() );   
   std::auto_ptr< LorentzV > topStop1 ( new LorentzV() );
   std::auto_ptr< LorentzV > topStop2 ( new LorentzV() );   
   //leptonic side of W form top from stop:  ~g -> ~t_1 t, ~t_1 -> chi0 t (b l nu)
   std::auto_ptr< LorentzV > bStop1      ( new LorentzV() );
   std::auto_ptr< LorentzV > bStop2      ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoLepStop1 ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoLepStop2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep1Stop1   ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep2Stop1   ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep1Stop2   ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep2Stop2   ( new LorentzV() );
   //leptonic side of W form top from stop:  ~g -> ~t_1 t, ~t_1 -> chi0 c

   //hadronic side of W from top from stop:  ~g -> ~t_1 t, ~t_1 -> chi0 t (b q q)
   std::auto_ptr< LorentzV > bG1         ( new LorentzV() );
   std::auto_ptr< LorentzV > bG2         ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoHadStop1 ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoHadStop2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Had1Stop1   ( new LorentzV() );
   std::auto_ptr< LorentzV > Had2Stop1   ( new LorentzV() );
   std::auto_ptr< LorentzV > Had1Stop2   ( new LorentzV() );
   std::auto_ptr< LorentzV > Had2Stop2   ( new LorentzV() );

   // top products
   // -------------
   std::auto_ptr< LorentzV > topG1 ( new LorentzV() );
   std::auto_ptr< LorentzV > topG2 ( new LorentzV() );
   //leptonic side of W form top from stop:  ~g -> ~t_1 (b l nu)
   std::auto_ptr< LorentzV > WtoLepG1 ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoLepG2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep1G1 ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep1G2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep2G1 ( new LorentzV() );
   std::auto_ptr< LorentzV > Lep2G2 ( new LorentzV() );
   //hadronic side of W from top from stop:  ~g -> ~t_1 (b q q)
   std::auto_ptr< LorentzV > WtoHadG1 ( new LorentzV() );
   std::auto_ptr< LorentzV > WtoHadG2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Had1G1 ( new LorentzV() );
   std::auto_ptr< LorentzV > Had1G2 ( new LorentzV() );
   std::auto_ptr< LorentzV > Had2G1 ( new LorentzV() );
   std::auto_ptr< LorentzV > Had2G2 ( new LorentzV() );
   
   if(!event.isRealData()){
      edm::Handle<std::vector<reco::GenParticle> > h_gen;
      event.getByLabel(edm::InputTag("prunedGenParticles"), h_gen); 
      assert ( h_gen.isValid() );

      std::vector<const reco::Candidate *> Stop(4); //~g->t t_1, t_1 -> chi0 t; (0,1) for gluino1 and (2,3) for gluino2  
      std::vector<const reco::Candidate *> Top(2);  //~g->t t_1
      std::vector<const reco::Candidate *> WtoLep(4); //  W -> l nu;  (0,1) for W <- t <- t_1 <- g~; (2,3) for W <- t <- g~
      std::vector<const reco::Candidate *> TtoWtoLep1(4); //W -> l
      std::vector<const reco::Candidate *> TtoWtoLep2(4); //W -> nu
      std::vector<const reco::Candidate *> WtoHad(4); //  W -> q q;   (0,1) for W <- t <- t_1 <- g~; (2,3) for W <- t <- g~
      std::vector<const reco::Candidate *> TtoWtoHad1(4); //W -> q1
      std::vector<const reco::Candidate *> TtoWtoHad2(4); //W -> q2
      std::vector<const reco::Candidate *> Ttob(4);      //  t -> b W;   (0,1) for t <- t_1 <- g~; (2,3) for t <- g~
 
      int numDa; int numChi0(0);
      setPointers(Stop); setPointers(Top); setPointers(WtoLep); setPointers(WtoHad);
      setPointers(TtoWtoLep1); setPointers(TtoWtoLep2); 
      setPointers(TtoWtoHad1);  setPointers(TtoWtoHad2);
      setPointers(Ttob);
    
      for (vector< reco::GenParticle>::const_iterator gpIter = h_gen->begin(); 
           gpIter != h_gen->end(); ++gpIter){
         
         if( gpIter->status() !=3) continue;
         numDa = gpIter->numberOfDaughters();   
         
         //select a gluino gluino event
         if(numDa >= 2 && abs(gpIter->daughter(0)->pdgId()) == 1000021 && abs(gpIter->daughter(1)->pdgId()) == 1000021 ){
            cout << "found a gluino pair " << endl;
            const reco::Candidate* gluinos[2] = { gpIter->daughter(0), gpIter->daughter(1) };
            
            //~g~g->~t_1~t_1tt
            for(int gl=0; gl<2; gl++){
                         
               if(gluinos[gl]->numberOfDaughters()<2){ std::cout << "gluino doesn't decay into 2 particles" << std::endl;  break;}    

               int numDau = gluinos[gl]->numberOfDaughters(); 
               for(int di=0; di<numDau; di++){ 

                  //~g->t t_1
                  if( gluinos[gl]->daughter(di)->status() != 3 ) continue;  
                  
                  //  //--------stop decay (t_1 -> chi0 t)--------
                  if(abs(gluinos[gl]->daughter(di)->pdgId()) == 1000006 && di < 2){      
 
                     if(gluinos[gl]->daughter(di)->numberOfDaughters()!=2) {cout << " stop doesn't decay into 2 particles!" << endl; break;}

                     if(abs(gluinos[gl]->daughter(di)->daughter(0)->pdgId())==1000022 && abs(gluinos[gl]->daughter(di)->daughter(1)->pdgId())==6){
                         numChi0++;
                         int numTopDau_stop =  gluinos[gl]->daughter(di)->daughter(1)->numberOfDaughters();
                         if (numChi0 == 1 ){
                            Stop[0] =  gluinos[gl]->daughter(di)->daughter(0);
                            Stop[2] =  gluinos[gl]->daughter(di)->daughter(1);
                            topDecay( Stop[2], numTopDau_stop, WtoLep[0], WtoHad[0], TtoWtoLep1[0], TtoWtoLep2[0], TtoWtoHad1[0],TtoWtoHad2[0], Ttob[0]);
                         }
                         else {// other gluino
                            Stop[1] =  gluinos[gl]->daughter(di)->daughter(0);
                            Stop[3] =  gluinos[gl]->daughter(di)->daughter(1);  
                            topDecay( Stop[3], numTopDau_stop, WtoLep[1], WtoHad[1], TtoWtoLep1[1], TtoWtoLep2[1], TtoWtoHad1[1],TtoWtoHad2[1], Ttob[1]);                         
                         }
                     }
                  }// t_1 decay

                  //-----top decay from gluino--------
                  if (abs(gluinos[gl]->daughter((di+1)%2)->pdgId()) == 6){
                       int numTopDau_gluino = gluinos[gl]->daughter((di+1)%2)->numberOfDaughters();
                        if (numChi0 == 1 ){
                           Top[0] = gluinos[gl]->daughter((di+1)%2);
                           topDecay( Top[0], numTopDau_gluino, WtoLep[2], WtoHad[2], TtoWtoLep1[2], TtoWtoLep2[2], TtoWtoHad1[2],TtoWtoHad2[2], Ttob[2]);
                        }
                        else{
                           Top[1] = gluinos[gl]->daughter((di+1)%2);
                           topDecay( Top[1], numTopDau_gluino, WtoLep[3], WtoHad[3], TtoWtoLep1[3], TtoWtoLep2[3], TtoWtoHad1[3],TtoWtoHad2[3], Ttob[3]);
                        }
                  }
                      
               }// loop over gluino daughters, di
            }// loop over gluino pair
            break; // if we find one g~g~ pair, lets stop the loop
         }// at least 2 daughters       
         
      }//gpIter
 

//     ~g1 decay products                
//     ==================
      //Stop products
      if(Stop[0] != 0)       {*chi0G1      = Stop[0]->p4(); }
      if(Stop[2] != 0)       {*topStop1    = Stop[2]->p4(); }
      if(Ttob[0]!=0 )        {*bStop1      = Ttob[0]->p4(); }
      if(WtoLep[0] != 0)     {*WtoLepStop1 = WtoLep[0]->p4(); } 
      if(TtoWtoLep1[0] != 0) {*Lep1Stop1   = TtoWtoLep1[0]->p4();}
      if(TtoWtoLep2[0] != 0) {*Lep2Stop1   = TtoWtoLep2[0]->p4();}
      if(WtoHad[0] != 0)     {*WtoHadStop1 = WtoHad[0]->p4(); }
      if(TtoWtoHad1[0] != 0) {*Had1Stop1   = TtoWtoHad1[0]->p4();}
      if(TtoWtoHad2[0] != 0) {*Had2Stop1   = TtoWtoHad2[0]->p4();}
      //Top products
      if(Top[0] != 0)        {*topG1       = Top[0]->p4(); }
      if(Ttob[2] !=0)        {*bG1         = Ttob[2]->p4(); }
      if(WtoLep[2] !=0)      {*WtoLepG1    = WtoLep[2]->p4();}
      if(TtoWtoLep1[2] !=0)  {*Lep1G1      = TtoWtoLep1[2]->p4();}
      if(TtoWtoLep2[2] !=0)  {*Lep2G1      = TtoWtoLep2[2]->p4();}
      if(WtoHad[2] !=0)      {*WtoHadG1    = WtoHad[2]->p4();}
      if(TtoWtoHad1[2] !=0)  {*Had1G1      = TtoWtoHad1[2]->p4();}
      if(TtoWtoHad2[2] !=0)  {*Had2G1      = TtoWtoHad2[2]->p4();}

//     ~g2 decay products
//     ====================
      //Stop products
      if(Stop[1] != 0)       {*chi0G2      = Stop[1]->p4();}
      if(Stop[3] != 0)       {*topStop2    = Stop[3]->p4();}
      if(Ttob[1] != 0)       {*bStop2      = Ttob[1]->p4();}
      if(WtoLep[1] != 0)     {*WtoLepStop2 = WtoLep[1]->p4(); }
      if(TtoWtoLep1[1] != 0) {*Lep1Stop2   = TtoWtoLep1[1]->p4();}
      if(TtoWtoLep2[1] != 0) {*Lep2Stop2   = TtoWtoLep2[1]->p4();}
      if(WtoHad[1] !=0 )     {*WtoHadStop2 = WtoHad[1]->p4();}
      if(TtoWtoHad1[1] != 0) {*Had1Stop2   = TtoWtoHad1[1]->p4();}
      if(TtoWtoHad2[1] != 0) {*Had2Stop2   = TtoWtoHad2[1]->p4();}
      //Top products       
      if(Top[1] != 0)        {*topG2       = Top[1]->p4();}
      if(Ttob[3] != 0)       {*bG2         = Ttob[3]->p4(); }
      if(WtoLep[3] !=0)      {*WtoLepG2    = WtoLep[3]->p4();}
      if(TtoWtoLep1[3] !=0)  {*Lep1G2      = TtoWtoLep1[3]->p4();}
      if(TtoWtoLep2[3] !=0)  {*Lep2G2      = TtoWtoLep2[3]->p4();}
      if(WtoHad[3] !=0)      {*WtoHadG2    = WtoHad[3]->p4();}
      if(TtoWtoHad1[3] !=0)  {*Had1G2      = TtoWtoHad1[3]->p4();}
      if(TtoWtoHad2[3] !=0)  {*Had2G2      = TtoWtoHad2[3]->p4();}

/*
      cout << "chi0 pt from 1st glu = " << Stop[0]->p4().pt() << ", top pt from 1st stop = " <<  Stop[2]->p4().pt() << ", top pt from 1st gluino = " <<  Top[0]->p4().pt() << endl;
      cout << "chi0 pt from 2nd glu = " << Stop[1]->p4().pt() << ", top pt from 2nd stop = " <<  Stop[3]->p4().pt() << ", top pt from 2nd gluino = " <<  Top[1]->p4().pt() << endl;
      
      for(unsigned i=0; i <4; ++i ){
         cout << "i: " << i << endl;
         if (numChi0 > 0){ 
            if (Stop[i] !=0 )        cout << " stop[" <<i<<"]: " << Stop[i]->p4().pt() <<" pdgId: " << Stop[i]->pdgId() << endl; 
            if (WtoLep[i] != 0 )  cout << " WtoLep[" << i << "]: " <<  WtoLep[i]->p4().pt() << " pdgId: " << WtoLep[i]->pdgId() << endl;  
            if (WtoHad[i] != 0 )  cout << " WtoHad[" << i << "]: " <<  WtoHad[i]->p4().pt() << " pdgId: " << WtoHad[i]->pdgId() << endl;            
            if (TtoWtoLep1[i] != 0 )  cout << " TtoWtoLep1[" << i << "]: " <<  TtoWtoLep1[i]->p4().pt() << " pdgId: " << TtoWtoLep1[i]->pdgId() << endl;
            if (TtoWtoLep2[i] != 0 )  cout << " TtoWtoLep2[" << i << "]: " <<  TtoWtoLep2[i]->p4().pt() << " pdgId: " << TtoWtoLep2[i]->pdgId() << endl;
            if (TtoWtoHad1[i] != 0 )  cout << " TtoWtoHad1[" << i << "]: " <<  TtoWtoHad1[i]->p4().pt() << " pdgId: " << TtoWtoHad1[i]->pdgId() << endl;
            if (TtoWtoHad2[i] != 0 )  cout << " TtoWtoHad2[" << i << "]: " <<  TtoWtoHad2[i]->p4().pt() << " pdgId: " << TtoWtoHad2[i]->pdgId() << endl;
            if (Ttob[i] != 0 )       cout << " Ttob[" << i << "]: " <<  Ttob[i]->p4().pt() << " pdgId: " << Ttob[i]->pdgId() << endl;           
         }
         
      }
*/  
   }  
   event.put ( chi0G1, "chi0G1");
   event.put ( topStop1, "topStop1");
   event.put ( bStop1, "bStop1");
   event.put ( WtoLepStop1, "WtoLepStop1");
   event.put ( Lep1Stop1, "Lep1Stop1");
   event.put ( Lep2Stop1, "Lep2Stop1");
   event.put ( WtoHadStop1, "WtoHadStop1");
   event.put ( Had1Stop1, "Had1Stop1");
   event.put ( Had2Stop1, "Had2Stop1"); 

   event.put ( topG1, "topG1"); 
   event.put ( bG1, "bG1");   
   event.put ( WtoLepG1, "WtoLepG1");
   event.put ( Lep1G1, "Lep1G1");
   event.put ( Lep2G1, "Lep2G1");
   event.put ( WtoHadG1, "WtoHadG1");
   event.put ( Had1G1, "Had1G1");

// other gluino
   event.put ( chi0G2, "chi0G2");
   event.put ( topStop2, "topStop2");
   event.put ( bStop2, "bStop2");
   event.put ( WtoLepStop2, "WtoLepStop2");
   event.put ( Lep1Stop2, "Lep1Stop2");
   event.put ( Lep2Stop2, "Lep2Stop2");
   event.put ( WtoHadStop2, "WtoHadStop2");
   event.put ( Had1Stop2, "Had1Stop2");
   event.put ( Had2Stop2, "Had2Stop2"); 
 
   event.put ( topG2, "topG2"); 
   event.put ( bG2, "bG2"); 
   event.put ( WtoLepG2, "WtoLepG2");
   event.put ( Lep1G2, "Lep1G2");
   event.put ( Lep2G2, "Lep2G2");
   event.put ( WtoHadG2, "WtoHadG2");
   event.put ( Had1G2, "Had1G2");
   
}

void BoostedSusy::topDecay(const reco::Candidate* top, int TopDau, const reco::Candidate* &WtoLep, const reco::Candidate* &WtoHad, 
                           const reco::Candidate* &TtoWtoLep1,  const reco::Candidate* &TtoWtoLep2,
                           const reco::Candidate* &TtoWtoHad1, const reco::Candidate* &TtoWtoHad2,
                           const reco::Candidate* &Ttob){

    for (int td=0; td<TopDau; td++){
       if (top->daughter(td)->status() != 3) continue;

       //cout << "td: paticle = " <<td  << ", " << top->daughter(td)->pdgId() << endl;
       
       //t -> W b
       if (abs(top->daughter(td)->pdgId()) == 24){                              
          
          if(top->daughter(td)->numberOfDaughters()!=2) {cout << "~t1->t->W, W doesn't decay into 2 particles!" << endl; break;}

          //find if the given W decays leptonicaly or hadronically
          if (abs(top->daughter(td)->daughter(0)->pdgId()) > 10){//W -> l nu
             //cout << "found W, ~t1->t->W->l nu " << endl;
             WtoLep = top->daughter(td);
             TtoWtoLep1 = top->daughter(td)->daughter(0);
             TtoWtoLep2 = top->daughter(td)->daughter(1);
          }
          else if (abs(top->daughter(td)->daughter(0)->pdgId()) < 6 &&
                   abs(top->daughter(td)->daughter(1)->pdgId()) < 6  ){//W -> qq
             //cout << "found W, ~t1->t->W->q q " << endl;
             WtoHad = top->daughter(td);
             TtoWtoHad1 = top->daughter(td)->daughter(0);
             TtoWtoHad2 = top->daughter(td)->daughter(1);
          }
                      
          if (abs(top->daughter((td+1)%2)->pdgId()) == 5 || abs(top->daughter((td+1)%2)->pdgId()) == 3 || abs(top->daughter((td+1)%2)->pdgId()) == 1) {//b, d, s
             //cout << "found b,  ~t1->t->b " << endl;
             Ttob = top->daughter((td+1)%2);
          } 
       
       }       
    }

}

void BoostedSusy::setPointers(std::vector<const reco::Candidate *> decayList){
   for(vector<const reco::Candidate *>::iterator iter = decayList.begin(); decayList.end() != iter; ++iter){
      *iter = 0;
   }
}

//define this as a plug-in
DEFINE_FWK_MODULE(BoostedSusy);
