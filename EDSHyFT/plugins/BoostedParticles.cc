/////////////////////////////////
// Class to study the semileptonic decay of b' decay:
// It stores the P4 of the decay products
//
////////////////////////////////
#include <memory>
#include "Analysis/EDSHyFT/plugins/BoostedParticles.h"

using namespace std;
using namespace edm;
using namespace reco;

void BoostedParticles::produce(edm::Event& event, const edm::EventSetup& setup)
{
   std::auto_ptr< LorentzV > Lep(new LorentzV() ) ;
   std::auto_ptr< LorentzV > Nu(new LorentzV() ) ;
   std::auto_ptr< LorentzV > LepT(new LorentzV() );
   std::auto_ptr< LorentzV > HadT(new LorentzV() );
   std::auto_ptr< LorentzV > WPart1(new LorentzV() ) ;
   std::auto_ptr< LorentzV > WPart2(new LorentzV() ) ;
   
   std::auto_ptr< LorentzV > HadTtoW(new LorentzV() );
   std::auto_ptr< LorentzV > HadTtob(new LorentzV() );
   std::auto_ptr< LorentzV > LepTtoW(new LorentzV() );
   std::auto_ptr< LorentzV > LepTtob(new LorentzV() );

   std::auto_ptr< bool >  bprimeSemileptonic(new bool (0));
   std::auto_ptr< bool >  bprimeDileptonic(new bool (0));
   std::auto_ptr< bool >  bprimeHadronic(new bool (0));
   std::auto_ptr< bool >  pureSemileptonicEvent(new bool (0));

   if(!event.isRealData()){
      edm::Handle<std::vector<reco::GenParticle> > h_gen;
      event.getByLabel(edm::InputTag("prunedGenParticles"), h_gen); 
      assert ( h_gen.isValid() );

      int numDa; int id(0); bool hasLepWt(0); bool hasHadWt(0); bool hasLepWtLepW(0); bool hasLepWtHadW(0); bool hasHadWtLepW(0); bool hasHadWtHadW(0);
      bool semileptonic(0), dileptonic(0), hadronic(0);      
      
      for (vector< reco::GenParticle>::const_iterator gpIter = h_gen->begin(); 
           gpIter != h_gen->end(); ++gpIter, ++id){

         if( gpIter->status() !=3) continue;
         numDa = gpIter->numberOfDaughters();   
        
         //select a b' b' event
         if(numDa >= 2 && abs(gpIter->daughter(0)->pdgId()) == 7 && abs(gpIter->daughter(1)->pdgId()) == 7 ){
            //cout << "found a b'b' event "<< endl;           
            const reco::Candidate* bprimes[2] = { gpIter->daughter(0), gpIter->daughter(1) };
        
            // check if this b'b' has a semileptonic decay
            for(int bi=0; bi<2; bi++){

               if(bprimes[bi]->numberOfDaughters()<2){ std::cout << "bprime doesn't decay into 2 particles" << std::endl;  break;}              
               BBtotWtW(bprimes[bi], hasLepWt, hasHadWt, hasLepWtLepW, hasLepWtHadW, hasHadWtLepW, hasHadWtHadW,
                        *Lep, *Nu, *LepT, *HadT, *WPart1, *WPart2, *HadTtoW, *HadTtob, *LepTtoW, * LepTtob); 
              
            }//bi
            break; // if we find one b'b' pair, lets stop the loop
         }// at least 2 daughters       
              
      }//gpIter

      //categorize the bprime event:
      if (hasLepWt == 1 && hasHadWt == 1){
         //cout  << "b'->tW: Semileptonic W decay " << endl;
         *bprimeSemileptonic = true;
         semileptonic = true;
      }
      else if (hasLepWt == 1 && hasHadWt == 0){
         //cout  << "b'->tW: Dileptonic W decay " << endl;
         *bprimeDileptonic = true;
         dileptonic = true;
      }
      else if (hasLepWt == 0 && hasHadWt == 1){
         //cout  << "b'->tW: Hadronic W decay " << endl;
         *bprimeHadronic = true;
         hadronic = true;
      }
      else {cout << " absurd, b' has to decay!" << endl; }

      
      
      //categorize the top decay and hence the full event
      //cout << "top decay: hasLepWtLepW == " << hasLepWtLepW <<",hasLepWtHadW == " << hasLepWtHadW << endl;
      //cout << "top decay: hasHadWtLepW == " << hasHadWtLepW <<",hasHadWtHadW == " << hasHadWtHadW << endl;

     
      if ( (semileptonic && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 2 ) || 
           (hadronic     && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 2 ) ){
         *pureSemileptonicEvent = true;
         // cout << "pure semileptonic event" << endl;
      }
      else if ( (hadronic && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 1 ) ){
         //  cout << "pure hadronic event" << endl;
      }
      else if ( (semileptonic && (hasLepWtLepW + hasHadWtLepW) == 1)                               ||
           (dileptonic   && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 1) ||
           (hadronic     && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 1) ){//
         // cout << "pure dileptonic event" << endl;
      }
      else if ( (semileptonic && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 3 ) ||//
           (dileptonic   && (hasLepWtLepW + hasHadWtLepW + hasLepWtHadW + hasHadWtHadW) == 2 ) ){
         //  cout << "pure multileptonic event" << endl;
      }

   }

  
   event.put ( Lep, "Lep");   
   event.put ( Nu, "Nu"); 
   event.put ( LepT, "LepT");
   event.put ( HadT, "HadT");
   event.put ( WPart1, "WPart1");
   event.put ( WPart2, "WPart2");
   event.put ( HadTtoW, "HadTtoW");
   event.put ( HadTtob, "HadTtob");
   event.put ( LepTtoW, "LepTtoW");
   event.put ( LepTtob, "LepTtob");
   event.put ( bprimeSemileptonic, "bprimeSemileptoni");
   event.put ( bprimeDileptonic, "bprimeDileptonic");
   event.put ( bprimeHadronic, "bprimeHadronic");
   event.put ( pureSemileptonicEvent, "pureSemileptonicEvent");
}

void BoostedParticles::BBtotWtW(const reco::Candidate* bprimes,bool&  hasLepWt, bool&  hasHadWt,
                                bool& hasLepWtLepW, bool& hasLepWtHadW, bool& hasHadWtLepW, bool& hasHadWtHadW,
                                LorentzV& Lep, LorentzV& Nu, LorentzV& LepT, 
                                LorentzV& HadT, LorentzV& WPart1, LorentzV& WPart2,
                                LorentzV& HadTtoW, LorentzV& HadTtob, LorentzV& LepTtoW, LorentzV& LepTtob){
   
   int numDau = bprimes->numberOfDaughters(); 
   for(int di=0; di<numDau; di++){ 

      if( bprimes->daughter(di)->status() != 3 ) continue;           
      int numTopDau = bprimes->daughter((di+1)%2)->numberOfDaughters();

      //b'->t W
      if(abs(bprimes->daughter(di)->pdgId()) == 24 && di < 2){
         if(bprimes->daughter(di)->numberOfDaughters()!=2) {cout << "W doesn't decay into 2 particles!" << endl; break;}

         //--------leptonic side--------
         if(abs(bprimes->daughter(di)->daughter(0)->pdgId())>10){
            //cout << "W decays leptonically " << endl;
            if(abs(bprimes->daughter(di)->daughter(0)->pdgId())%2==0) {//W+ -> l+ nu
               Lep = bprimes->daughter(di)->daughter(1)->polarP4(); 
               Nu = bprimes->daughter(di)->daughter(0)->polarP4();
            }
            else {//W- -> l- nu
               Lep = bprimes->daughter(di)->daughter(0)->polarP4(); 
               Nu = bprimes->daughter(di)->daughter(1)->polarP4();
            }
            //fill the other leg, t quark
            if(abs(bprimes->daughter((di+1)%2)->pdgId())!=6){std::cout << "leptonic side W does not have brother t quark!" << std::endl; break;}
            LepT = bprimes->daughter((di+1)%2)->polarP4();
            hasLepWt=true;
            
            //--------The top decay---------
            for(int td=0; td<numTopDau; td++){
               if(bprimes->daughter((di+1)%2)->daughter(td)->status() != 3 ) continue;

               //t->W b
               if(abs(bprimes->daughter((di+1)%2)->daughter(td)->pdgId()) == 24 && td < 2){// t -> W
                  if(bprimes->daughter((di+1)%2)->daughter(td)->numberOfDaughters()!=2) {cout << "W doesn't decay into 2 particles!" << endl; break;}
                  LepTtoW = bprimes->daughter((di+1)%2)->daughter(td)->polarP4();

                  //find if the given W decays leptonicaly or hadronically
                  if(abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(0)->pdgId())>10) hasLepWtLepW=true; //W -> l nu
                  else if (abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(0)->pdgId())<6 && 
                           abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(1)->pdgId())<6);  hasLepWtHadW=true; //W  -> qq   

                  //the other b/q quark from top decay
                  if(abs(bprimes->daughter((di+1)%2)->daughter((td+1)%2)->pdgId())>5){std::cout << "W LepTtoW does not have brother b,d,s quark!" << std::endl; break;}
                  LepTtob = bprimes->daughter((di+1)%2)->daughter((td+1)%2)->polarP4();
              }
            }//td 

         } //------hadronic side--------
         else if(abs(bprimes->daughter(di)->daughter(0)->pdgId())<6 && abs(bprimes->daughter(di)->daughter(1)->pdgId())<6){ 
            //cout << "W decays hadronically " << endl;
            if(abs(bprimes->daughter(di)->daughter(0)->pdgId())%2==1){//W+ -> q q'bar
               WPart1 = bprimes->daughter(di)->daughter(0)->polarP4(); 
               WPart2 = bprimes->daughter(di)->daughter(1)->polarP4();
            }   
            else{//W- -> q'bar q
               WPart1 = bprimes->daughter(di)->daughter(1)->polarP4(); 
               WPart2 = bprimes->daughter(di)->daughter(0)->polarP4();
            }
            //fill the hadronic leg, t quark
            if(abs(bprimes->daughter((di+1)%2)->pdgId())!=6){std::cout << "hadronic side W does not have brother t quark!" << std::endl; break;}
            HadT = bprimes->daughter((di+1)%2)->polarP4();
            hasHadWt=true;
            
            //--------The top decay---------
            for(int td=0; td<numTopDau; td++){
               if(bprimes->daughter((di+1)%2)->daughter(td)->status() != 3 ) continue;

               //t->W b
               if(abs(bprimes->daughter((di+1)%2)->daughter(td)->pdgId()) == 24 && td < 2){// t -> W
                  if(bprimes->daughter((di+1)%2)->daughter(td)->numberOfDaughters()!=2) {cout << "W doesn't decay into 2 particles!" << endl; break;}
                  HadTtoW = bprimes->daughter((di+1)%2)->daughter(td)->polarP4();
                 
                  //find if the given W decays leptonicaly or hadronically
                  if(abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(0)->pdgId())>10) hasHadWtLepW=true; //W -> l nu  
                  else if (abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(0)->pdgId())<6 && 
                           abs(bprimes->daughter((di+1)%2)->daughter(td)->daughter(1)->pdgId())<6) hasHadWtHadW=true; //W  -> qq

                  //the other b/q quark from top
                  if(abs(bprimes->daughter((di+1)%2)->daughter((td+1)%2)->pdgId())>5){std::cout << "W HadTtoW does not have brother b,d,s quark!" << std::endl; break;}
                  HadTtob = bprimes->daughter((di+1)%2)->daughter((td+1)%2)->polarP4();
              }
            }//td 

         }//hadronic side
      
      }//b'->t W
     
   }//di
   //cout << "semileptonic inside: hasLepWt == " << hasLepWt <<",hasHadWt == " << hasHadWt << endl;
   //cout << "top decay inside: hasLepWtLepW == " << hasLepWtLepW <<",hasLepWtHadW == " << hasLepWtHadW << endl;
   //cout << "top decay inside: hasHadWtLepW == " << hasHadWtLepW <<",hasHadWtHadW == " << hasHadWtHadW << endl;
}


//define this as a plug-in
DEFINE_FWK_MODULE(BoostedParticles);
