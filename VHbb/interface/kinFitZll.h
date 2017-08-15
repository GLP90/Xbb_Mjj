#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TFitConstraintM.h"
#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TFitParticleEtEtaPhi.h"
#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TKinFitter.h"
#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TFitConstraintEp.h"
#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TAbsFitConstraint.h"
#include "TLorentzVector.h"
#include "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/PhysicsTools/KinFitter/interface/TFitParticleEScaledMomDev.h"
#include <iostream>

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// Modified version of the ExampleEtEtaPhi2CFit.C macro from CMS AN 2005/025.
// Jet error parametrization from CMS AN 2005/005.
//
// To run this macro in a root session do:
// root [0] gSystem->Load("libPhysicsToolsKinFitter.so");
// root [1] .x PhysicsTools/KinFitter/test/kinFitZll.C+
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
namespace HZll
{
double deltaPhi(double phi1,double phi2)
  {
    double result = phi1 - phi2;
    while (result > TMath::Pi()) result -= 2*TMath::Pi();
    while (result <= -TMath::Pi()) result += 2*TMath::Pi();
    return result;
  }

double deltaR(double eta1,double phi1,double eta2,double phi2)
    {
      double deta = eta1 - eta2;
      double dphi = deltaPhi(phi1, phi2);
      return TMath::Sqrt(deta*deta + dphi*dphi);
    }
/*
Double_t ErrEt(Float_t Et, Float_t Eta){
Double_t InvPerr2, a, b, c;
const int NYBINS = 5;
double YBND[NYBINS+1] = {0,0.5,1.0,1.5,2.0,2.5};
double PAR[NYBINS][3] = {
  {3.51, 0.826, 0.0364},{3.23, 0.851, 0.0367},{4.36, 0.871, 0.0415},
  {5.22, 0.713, 0.0229},{5.07, 0.610, 0.0207}};
int iy =0; 
if (fabs(Eta) < 2.5){
if (fabs(Eta) < 0.5 && fabs(Eta) >0.) iy =0;
if (fabs(Eta) < 1. && fabs(Eta) >0.5) iy =1;
if (fabs(Eta) < 1.5 && fabs(Eta) >1.) iy =2;
if (fabs(Eta) < 2. && fabs(Eta) >1.5) iy =3;
if (fabs(Eta) < 2. && fabs(Eta) >2.5) iy =4;
///std::cout<< iy << " kin  iy "<<std::endl;

InvPerr2 = sqrt(pow(PAR[iy][0]/Et,2) + pow(PAR[iy][1],2)/Et + pow(PAR[iy][2],2));
//std::cout<< InvPerr2 << " kin  invPerr "<<std::endl;
}
else if(fabs(Eta) >= 2.5){
  a = 4.8;
  b = 0.89;
  c = 0.043; 
  InvPerr2 = (a * a) + (b * b) * Et + (c * c) * Et * Et;	
} 

return InvPerr2;
}
*/
Double_t ErrEt(Float_t Et, Float_t Eta) {
  Double_t InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 5.6;
    b = 1.25;
    c = 0.033;
  }
  else{
    a = 4.8;
    b = 0.89;
    c = 0.043;
  }
  InvPerr2 = (a * a) + (b * b) * Et + (c * c) * Et * Et;
  return InvPerr2;
}

Double_t ErrEta(Float_t Et, Float_t Eta) {
  Double_t InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 1.215;
    b = 0.037;
    c = 7.941 * 0.0001;
  }
  else{
    a = 1.773;
    b = 0.034;
    c = 3.56 * 0.0001;
  }
 InvPerr2 = a/(Et * Et) + b/Et + c;
 
return InvPerr2;
}

Double_t ErrPhi(Float_t Et, Float_t Eta) {
  Double_t InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 6.65;
    b = 0.04;
    c = 8.49 * 0.00001;
  }
  else{
    a = 2.908;
    b = 0.021;
    c = 2.59 * 0.0001;
  }
 InvPerr2 = a/(Et * Et) + b/Et + c;
return InvPerr2;
}


float chi2(TLorentzVector v1, TLorentzVector v2){

  float result = -1;

  TMatrixD m1(3,3);
  TMatrixD m2(3,3);
  m1.Zero();
  m2.Zero();
  
  //In this example the covariant matrix depends on the transverse energy and eta of the jets
  m1(0,0) = ErrEt (v1.Et(), v1.Eta()); // et
  m1(1,1) = ErrEta(v1.Et(), v1.Eta()); // eta
  m1(2,2) = ErrPhi(v1.Et(), v1.Eta()); // phi
  m2(0,0) = ErrEt (v2.Et(), v2.Eta()); // et
  m2(1,1) = ErrEta(v2.Et(), v2.Eta()); // eta
  m2(2,2) = ErrPhi(v2.Et(), v2.Eta()); // phi
  
  TFitParticleEtEtaPhi *jet1 = new TFitParticleEtEtaPhi( "Jet1", "Jet1", &v1, &m1 );
  TFitParticleEtEtaPhi *jet2 = new TFitParticleEtEtaPhi( "Jet2", "Jet2", &v2, &m2 );
  
  TFitConstraintM *mCons1 = new TFitConstraintM( "WMassConstraint", "WMass-Constraint", 0, 0 , 125);
  mCons1->addParticles1( jet1, jet2 );

  //Definition of the fitter
  //Add two measured particles(jets)
  //Add one mass constraint
  TKinFitter* fitter = new TKinFitter("fitter", "fitter");
  fitter -> addMeasParticle( jet1 );
  fitter -> addMeasParticle( jet2 );
  fitter -> addConstraint( mCons1 );

  //Set convergence criteria
  fitter->setMaxNbIter(200);
  fitter->setMaxDeltaS(5e-5);
  fitter->setMaxF(1e-4);
  fitter->setVerbosity(0);

  //Perform the fit
  fitter -> fit();
  
  // result = fitter -> getS(); 
  
  // get the mass
  const TLorentzVector* jet1F;
  const TLorentzVector* jet2F;

  jet1F = fitter -> get4Vec(0);
  jet2F = fitter -> get4Vec(1);

  TLorentzVector H1;

  H1 = *jet1F + *jet2F;
  
  double H1_mass = H1.M();

  delete jet1;
  delete jet2;
  delete mCons1;
  delete fitter;

  return H1_mass;

}



// ===== Used to predict the diJet pt values =======
TLorentzVector Xchi2(TLorentzVector &l11, TLorentzVector &l22,TLorentzVector &v11, TLorentzVector &v22, double px, double py){
  
  // Jet vectors
  TLorentzVector v1 = v11;
  TLorentzVector v2 = v22;
  
  // lepton vectors
  TLorentzVector l1 = l11;
  TLorentzVector l2 = l22;
  

  TMatrixD m1(3,3);
  TMatrixD m2(3,3);
  TMatrixD mm1(3,3);
  TMatrixD mm2(3,3);
  TMatrixD m6(3,3);	

  mm1.Zero();
  mm2.Zero();
  m1.Zero();
  m2.Zero();

  m6.Zero();	
  
  //In this example the covariant matrix depends on the transverse energy and eta of the jets

  m1(0,0) = ErrEt (v1.Et(), v1.Eta()); // et
  m1(1,1) = ErrEta(v1.Et(), v1.Eta()); // eta
  m1(2,2) = ErrPhi(v1.Et(), v1.Eta()); // phi
  
  mm1(0,0) = ErrEt (l1.Et(), l1.Eta()); // et
  mm1(1,1) = ErrEta(l1.Et(), l1.Eta()); // eta
  mm1(2,2) = ErrPhi(l1.Et(), l1.Eta()); // phi

  m2(0,0) = ErrEt (v2.Et(), v2.Eta()); // et
  m2(1,1) = ErrEta(v2.Et(), v2.Eta()); // eta
  m2(2,2) = ErrPhi(v2.Et(), v2.Eta()); // phi

  mm2(0,0) = ErrEt (l2.Et(), l2.Eta()); // et
  mm2(1,1) = ErrEta(l2.Et(), l2.Eta()); // eta
  mm2(2,2) = ErrPhi(l2.Et(), l2.Eta()); // phi

  m6(0,0) = 15; m6(1,1) =15; m6(2,2) = 9999;//pow(0.54, 2);
  

  /*
  m1(0,0) = 10;
  m1(1,1) = 10;
  m1(2,2) = 10;

  mm1(0,0) = 10;
  mm1(1,1) = 10;
  mm1(2,2) = 10;

  m2(0,0) = 10;
  m2(1,1) = 10;
  m2(2,2) = 10;

  mm2(0,0) = 10;
  mm2(1,1) = 10;
  mm2(2,2) = 10;
  */
  


  TFitParticleEtEtaPhi *jet1 = new TFitParticleEtEtaPhi( "Jet1", "Jet1", &v1, &m1 );
  TFitParticleEtEtaPhi *jet2 = new TFitParticleEtEtaPhi( "Jet2", "Jet2", &v2, &m2 );
  TFitParticleEtEtaPhi *lep1 = new TFitParticleEtEtaPhi( "Lep1", "Lep1", &l1, &mm1 );
  TFitParticleEtEtaPhi *lep2 = new TFitParticleEtEtaPhi( "Lep2", "Lep2", &l2, &mm2 );
  
  //constrain the transverse momentum
  TFitConstraintEp *ConsX = new TFitConstraintEp( "ConstraintX","ConstraintX" , TFitConstraintEp::pX, px );	
  TFitConstraintEp *ConsY = new TFitConstraintEp( "ConstraintY","ConstraintY" , TFitConstraintEp::pY, py );
  ConsX->addParticles( jet1, jet2 , lep1, lep2 );
  ConsY->addParticles( jet1, jet2 , lep1, lep2 );
  
  TKinFitter* fitter = new TKinFitter("fitter", "fitter");
  fitter -> addMeasParticle(jet1);
  fitter -> addMeasParticle(jet2);
  //fitter -> addMeasParticle(neutrino);
  fitter -> addMeasParticle(lep2);
  fitter -> addMeasParticle(lep1);	
  fitter -> addConstraint(ConsX);
  fitter -> addConstraint(ConsY);
  //fitter -> addConstraint(mCons1);
  
  //Set convergence criteria
  fitter->setMaxNbIter( 10 );
  fitter->setMaxDeltaS( 1e-2 );
  fitter->setMaxF( 1e-1 );
  fitter->setVerbosity(1);
  
  //Perform the fit
  fitter->fit();
  
  //chi2 = fitter->getS();
  // std::cout<< chi2 << std::endl;
  const TLorentzVector* jet1F;
  const TLorentzVector* jet2F;
  
  jet1F = fitter -> get4Vec(0);
  jet2F = fitter -> get4Vec(1);
  
  TLorentzVector H1;
  v11= *jet1F;
  v22= *jet2F;
  
  H1 = (*jet1F)+(*jet2F);	
  // std::cout<< H1.M() <<std::endl;	
  
  delete jet1;
  delete jet2;
  delete lep1;
  delete lep2;
  delete ConsX;
  delete ConsY;	
  delete fitter;
  
  //cout << "----> end Kin Fit" << endl;
  
  return H1.M();
	
  

  }

}
