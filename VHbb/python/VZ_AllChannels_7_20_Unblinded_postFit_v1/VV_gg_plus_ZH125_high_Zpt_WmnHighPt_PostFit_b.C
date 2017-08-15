void VV_gg_plus_ZH125_high_Zpt_WmnHighPt_PostFit_b()
{
//=========Macro generated from canvas: gg_plus_ZH125_high_Zpt/
//=========  (Sat Jul 22 20:26:21 2017) by ROOT version6.02/05
   TCanvas *gg_plus_ZH125_high_Zpt = new TCanvas("gg_plus_ZH125_high_Zpt", "",0,0,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   gg_plus_ZH125_high_Zpt->SetHighLightColor(2);
   gg_plus_ZH125_high_Zpt->Range(0,0,1,1);
   gg_plus_ZH125_high_Zpt->SetFillColor(0);
   gg_plus_ZH125_high_Zpt->SetFillStyle(4000);
   gg_plus_ZH125_high_Zpt->SetBorderMode(0);
   gg_plus_ZH125_high_Zpt->SetBorderSize(2);
   gg_plus_ZH125_high_Zpt->SetTickx(1);
   gg_plus_ZH125_high_Zpt->SetTicky(1);
   gg_plus_ZH125_high_Zpt->SetLeftMargin(0.13);
   gg_plus_ZH125_high_Zpt->SetRightMargin(0.05);
   gg_plus_ZH125_high_Zpt->SetTopMargin(0.05);
   gg_plus_ZH125_high_Zpt->SetBottomMargin(0.13);
   gg_plus_ZH125_high_Zpt->SetFrameFillStyle(1000);
   gg_plus_ZH125_high_Zpt->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: oben
   TPad *oben = new TPad("oben", "oben",0,0.3,1,1);
   oben->Draw();
   oben->cd();
   oben->Range(0.07317074,-1.716642,1.04878,8.347119);
   oben->SetFillColor(0);
   oben->SetFillStyle(4000);
   oben->SetBorderMode(0);
   oben->SetBorderSize(2);
   oben->SetLogy();
   oben->SetTickx(1);
   oben->SetTicky(1);
   oben->SetLeftMargin(0.13);
   oben->SetRightMargin(0.05);
   oben->SetTopMargin(0.05);
   oben->SetBottomMargin(0);
   oben->SetFrameFillStyle(1000);
   oben->SetFrameBorderMode(0);
   oben->SetFrameFillStyle(1000);
   oben->SetFrameBorderMode(0);
   
   THStack *gg_plus_ZH125_high_Zpt = new THStack();
   gg_plus_ZH125_high_Zpt->SetName("gg_plus_ZH125_high_Zpt");
   gg_plus_ZH125_high_Zpt->SetTitle("");
   gg_plus_ZH125_high_Zpt->SetMinimum(0.1);
   gg_plus_ZH125_high_Zpt->SetMaximum(2.601959e+07);
   
   TH1F *gg_plus_ZH125_high_Zpt_stack_1 = new TH1F("gg_plus_ZH125_high_Zpt_stack_1","",11,0.2,1);
   gg_plus_ZH125_high_Zpt_stack_1->SetMinimum(0.01920252);
   gg_plus_ZH125_high_Zpt_stack_1->SetMaximum(6.981212e+07);
   gg_plus_ZH125_high_Zpt_stack_1->SetDirectory(0);
   gg_plus_ZH125_high_Zpt_stack_1->SetStats(0);
   gg_plus_ZH125_high_Zpt_stack_1->SetFillColor(63);
   gg_plus_ZH125_high_Zpt_stack_1->SetLineStyle(0);
   gg_plus_ZH125_high_Zpt_stack_1->SetMarkerStyle(20);
   gg_plus_ZH125_high_Zpt_stack_1->SetMarkerSize(1.2);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetRange(1,11);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetLabelFont(42);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetLabelOffset(999);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetLabelSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetTitleSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetXaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetTitle("Entries / 0.07");
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetLabelFont(42);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetLabelOffset(0.007);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetLabelSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetTitleSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetTitleOffset(1.4);
   gg_plus_ZH125_high_Zpt_stack_1->GetYaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt_stack_1->GetZaxis()->SetLabelFont(42);
   gg_plus_ZH125_high_Zpt_stack_1->GetZaxis()->SetLabelOffset(0.007);
   gg_plus_ZH125_high_Zpt_stack_1->GetZaxis()->SetLabelSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetZaxis()->SetTitleSize(0.05);
   gg_plus_ZH125_high_Zpt_stack_1->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->SetHistogram(gg_plus_ZH125_high_Zpt_stack_1);
   
   
   TH1F *Wj2b1 = new TH1F("Wj2b1","Wj2b",11,0.2,1);
   Wj2b1->SetBinContent(1,204.9104);
   Wj2b1->SetBinContent(2,183.0749);
   Wj2b1->SetBinContent(3,152.9716);
   Wj2b1->SetBinContent(4,126.7514);
   Wj2b1->SetBinContent(5,48.42263);
   Wj2b1->SetBinContent(6,47.72648);
   Wj2b1->SetBinContent(7,33.90609);
   Wj2b1->SetBinContent(8,19.6332);
   Wj2b1->SetBinContent(9,9.50244);
   Wj2b1->SetBinContent(10,2.313097);
   Wj2b1->SetBinContent(11,0.1468579);
   Wj2b1->SetBinError(1,5.977174);
   Wj2b1->SetBinError(2,6.017877);
   Wj2b1->SetBinError(3,4.079136);
   Wj2b1->SetBinError(4,4.725333);
   Wj2b1->SetBinError(5,2.431876);
   Wj2b1->SetBinError(6,2.571474);
   Wj2b1->SetBinError(7,2.59579);
   Wj2b1->SetBinError(8,0.8512945);
   Wj2b1->SetBinError(9,0.572739);
   Wj2b1->SetBinError(10,0.2741964);
   Wj2b1->SetBinError(11,0.04233843);
   Wj2b1->SetEntries(11);
   Wj2b1->SetDirectory(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#00ff00");
   Wj2b1->SetFillColor(ci);
   Wj2b1->GetXaxis()->SetLabelFont(42);
   Wj2b1->GetXaxis()->SetLabelSize(0.035);
   Wj2b1->GetXaxis()->SetTitleSize(0.035);
   Wj2b1->GetXaxis()->SetTitleFont(42);
   Wj2b1->GetYaxis()->SetLabelFont(42);
   Wj2b1->GetYaxis()->SetLabelSize(0.035);
   Wj2b1->GetYaxis()->SetTitleSize(0.035);
   Wj2b1->GetYaxis()->SetTitleFont(42);
   Wj2b1->GetZaxis()->SetLabelFont(42);
   Wj2b1->GetZaxis()->SetLabelSize(0.035);
   Wj2b1->GetZaxis()->SetTitleSize(0.035);
   Wj2b1->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Wj2b,"");
   
   TH1F *WH_hbb2 = new TH1F("WH_hbb2","WH",11,0.2,1);
   WH_hbb2->SetBinContent(1,6.312504);
   WH_hbb2->SetBinContent(2,5.60927);
   WH_hbb2->SetBinContent(3,4.518902);
   WH_hbb2->SetBinContent(4,3.515334);
   WH_hbb2->SetBinContent(5,1.402693);
   WH_hbb2->SetBinContent(6,1.052753);
   WH_hbb2->SetBinContent(7,0.8070319);
   WH_hbb2->SetBinContent(8,0.5053026);
   WH_hbb2->SetBinContent(9,0.2463568);
   WH_hbb2->SetBinContent(10,0.04997625);
   WH_hbb2->SetBinContent(11,0.002012227);
   WH_hbb2->SetBinError(1,0.1607056);
   WH_hbb2->SetBinError(2,0.1488318);
   WH_hbb2->SetBinError(3,0.1342643);
   WH_hbb2->SetBinError(4,0.1168267);
   WH_hbb2->SetBinError(5,0.07278352);
   WH_hbb2->SetBinError(6,0.06189251);
   WH_hbb2->SetBinError(7,0.05633536);
   WH_hbb2->SetBinError(8,0.04250313);
   WH_hbb2->SetBinError(9,0.03040128);
   WH_hbb2->SetBinError(10,0.01187323);
   WH_hbb2->SetBinError(11,0.003901363);
   WH_hbb2->SetEntries(11);
   WH_hbb2->SetDirectory(0);
   WH_hbb2->SetFillColor(2);
   WH_hbb2->GetXaxis()->SetLabelFont(42);
   WH_hbb2->GetXaxis()->SetLabelSize(0.035);
   WH_hbb2->GetXaxis()->SetTitleSize(0.035);
   WH_hbb2->GetXaxis()->SetTitleFont(42);
   WH_hbb2->GetYaxis()->SetLabelFont(42);
   WH_hbb2->GetYaxis()->SetLabelSize(0.035);
   WH_hbb2->GetYaxis()->SetTitleSize(0.035);
   WH_hbb2->GetYaxis()->SetTitleFont(42);
   WH_hbb2->GetZaxis()->SetLabelFont(42);
   WH_hbb2->GetZaxis()->SetLabelSize(0.035);
   WH_hbb2->GetZaxis()->SetTitleSize(0.035);
   WH_hbb2->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(WH_hbb,"");
   
   TH1F *ZH_hbb3 = new TH1F("ZH_hbb3","ZH",11,0.2,1);
   ZH_hbb3->SetBinContent(1,0.2767086);
   ZH_hbb3->SetBinContent(2,0.1897026);
   ZH_hbb3->SetBinContent(3,0.1607006);
   ZH_hbb3->SetBinContent(4,0.1143767);
   ZH_hbb3->SetBinContent(5,0.04947463);
   ZH_hbb3->SetBinContent(6,0.03310658);
   ZH_hbb3->SetBinContent(7,0.01931175);
   ZH_hbb3->SetBinContent(8,0.01350447);
   ZH_hbb3->SetBinContent(9,0.005616245);
   ZH_hbb3->SetBinContent(10,0.001067818);
   ZH_hbb3->SetBinContent(11,8.635699e-10);
   ZH_hbb3->SetBinError(1,0.01822373);
   ZH_hbb3->SetBinError(2,0.01610482);
   ZH_hbb3->SetBinError(3,0.01398562);
   ZH_hbb3->SetBinError(4,0.01149473);
   ZH_hbb3->SetBinError(5,0.007435726);
   ZH_hbb3->SetBinError(6,0.006679022);
   ZH_hbb3->SetBinError(7,0.004665217);
   ZH_hbb3->SetBinError(8,0.003721134);
   ZH_hbb3->SetBinError(9,0.002077185);
   ZH_hbb3->SetBinError(10,0.001030039);
   ZH_hbb3->SetEntries(11);
   ZH_hbb3->SetDirectory(0);
   ZH_hbb3->SetFillColor(2);
   ZH_hbb3->GetXaxis()->SetLabelFont(42);
   ZH_hbb3->GetXaxis()->SetLabelSize(0.035);
   ZH_hbb3->GetXaxis()->SetTitleSize(0.035);
   ZH_hbb3->GetXaxis()->SetTitleFont(42);
   ZH_hbb3->GetYaxis()->SetLabelFont(42);
   ZH_hbb3->GetYaxis()->SetLabelSize(0.035);
   ZH_hbb3->GetYaxis()->SetTitleSize(0.035);
   ZH_hbb3->GetYaxis()->SetTitleFont(42);
   ZH_hbb3->GetZaxis()->SetLabelFont(42);
   ZH_hbb3->GetZaxis()->SetLabelSize(0.035);
   ZH_hbb3->GetZaxis()->SetTitleSize(0.035);
   ZH_hbb3->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(ZH_hbb,"");
   
   TH1F *Wj1b4 = new TH1F("Wj1b4","Wj1b",11,0.2,1);
   Wj1b4->SetBinContent(1,162.4823);
   Wj1b4->SetBinContent(2,155.3951);
   Wj1b4->SetBinContent(3,86.71192);
   Wj1b4->SetBinContent(4,45.6671);
   Wj1b4->SetBinContent(5,14.34803);
   Wj1b4->SetBinContent(6,9.344025);
   Wj1b4->SetBinContent(7,7.500841);
   Wj1b4->SetBinContent(8,3.117227);
   Wj1b4->SetBinContent(9,1.13289);
   Wj1b4->SetBinContent(10,0.4099986);
   Wj1b4->SetBinContent(11,0.0171021);
   Wj1b4->SetBinError(1,6.823878);
   Wj1b4->SetBinError(2,7.71664);
   Wj1b4->SetBinError(3,3.728156);
   Wj1b4->SetBinError(4,1.958211);
   Wj1b4->SetBinError(5,0.9667062);
   Wj1b4->SetBinError(6,0.6917459);
   Wj1b4->SetBinError(7,0.5250038);
   Wj1b4->SetBinError(8,0.4100524);
   Wj1b4->SetBinError(9,0.133075);
   Wj1b4->SetBinError(10,0.08179);
   Wj1b4->SetEntries(11);
   Wj1b4->SetDirectory(0);

   ci = TColor::GetColor("#66cc66");
   Wj1b4->SetFillColor(ci);
   Wj1b4->GetXaxis()->SetLabelFont(42);
   Wj1b4->GetXaxis()->SetLabelSize(0.035);
   Wj1b4->GetXaxis()->SetTitleSize(0.035);
   Wj1b4->GetXaxis()->SetTitleFont(42);
   Wj1b4->GetYaxis()->SetLabelFont(42);
   Wj1b4->GetYaxis()->SetLabelSize(0.035);
   Wj1b4->GetYaxis()->SetTitleSize(0.035);
   Wj1b4->GetYaxis()->SetTitleFont(42);
   Wj1b4->GetZaxis()->SetLabelFont(42);
   Wj1b4->GetZaxis()->SetLabelSize(0.035);
   Wj1b4->GetZaxis()->SetTitleSize(0.035);
   Wj1b4->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Wj1b,"");
   
   TH1F *Wj0b5 = new TH1F("Wj0b5","Wj0b",11,0.2,1);
   Wj0b5->SetBinContent(1,73.69861);
   Wj0b5->SetBinContent(2,78.28864);
   Wj0b5->SetBinContent(3,52.28318);
   Wj0b5->SetBinContent(4,37.33912);
   Wj0b5->SetBinContent(5,7.109221);
   Wj0b5->SetBinContent(6,3.520941);
   Wj0b5->SetBinContent(7,6.213583);
   Wj0b5->SetBinContent(8,0.2283385);
   Wj0b5->SetBinContent(9,0.1151214);
   Wj0b5->SetBinContent(10,0.1162459);
   Wj0b5->SetBinContent(11,2.58913e-07);
   Wj0b5->SetBinError(1,10.67733);
   Wj0b5->SetBinError(2,11.34241);
   Wj0b5->SetBinError(3,8.798148);
   Wj0b5->SetBinError(4,6.645615);
   Wj0b5->SetBinError(5,3.047601);
   Wj0b5->SetBinError(6,1.885669);
   Wj0b5->SetBinError(7,2.667577);
   Wj0b5->SetBinError(8,0.08817271);
   Wj0b5->SetBinError(9,0.06742084);
   Wj0b5->SetBinError(10,0.09495512);
   Wj0b5->SetEntries(11);
   Wj0b5->SetDirectory(0);

   ci = TColor::GetColor("#009900");
   Wj0b5->SetFillColor(ci);
   Wj0b5->GetXaxis()->SetLabelFont(42);
   Wj0b5->GetXaxis()->SetLabelSize(0.035);
   Wj0b5->GetXaxis()->SetTitleSize(0.035);
   Wj0b5->GetXaxis()->SetTitleFont(42);
   Wj0b5->GetYaxis()->SetLabelFont(42);
   Wj0b5->GetYaxis()->SetLabelSize(0.035);
   Wj0b5->GetYaxis()->SetTitleSize(0.035);
   Wj0b5->GetYaxis()->SetTitleFont(42);
   Wj0b5->GetZaxis()->SetLabelFont(42);
   Wj0b5->GetZaxis()->SetLabelSize(0.035);
   Wj0b5->GetZaxis()->SetTitleSize(0.035);
   Wj0b5->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Wj0b,"");
   
   TH1F *s_Top6 = new TH1F("s_Top6","s_Top",11,0.2,1);
   s_Top6->SetBinContent(1,339.2284);
   s_Top6->SetBinContent(2,266.5667);
   s_Top6->SetBinContent(3,195.185);
   s_Top6->SetBinContent(4,99.07385);
   s_Top6->SetBinContent(5,25.55418);
   s_Top6->SetBinContent(6,22.38896);
   s_Top6->SetBinContent(7,9.963503);
   s_Top6->SetBinContent(8,5.381027);
   s_Top6->SetBinContent(9,1.557371);
   s_Top6->SetBinContent(10,0.5083771);
   s_Top6->SetBinContent(11,9.654074e-07);
   s_Top6->SetBinError(1,8.762768);
   s_Top6->SetBinError(2,7.545412);
   s_Top6->SetBinError(3,6.421356);
   s_Top6->SetBinError(4,4.377837);
   s_Top6->SetBinError(5,2.32479);
   s_Top6->SetBinError(6,2.123675);
   s_Top6->SetBinError(7,1.463277);
   s_Top6->SetBinError(8,1.032382);
   s_Top6->SetBinError(9,0.4304961);
   s_Top6->SetBinError(10,0.3447419);
   s_Top6->SetEntries(11);
   s_Top6->SetDirectory(0);

   ci = TColor::GetColor("#00ffcc");
   s_Top6->SetFillColor(ci);
   s_Top6->GetXaxis()->SetLabelFont(42);
   s_Top6->GetXaxis()->SetLabelSize(0.035);
   s_Top6->GetXaxis()->SetTitleSize(0.035);
   s_Top6->GetXaxis()->SetTitleFont(42);
   s_Top6->GetYaxis()->SetLabelFont(42);
   s_Top6->GetYaxis()->SetLabelSize(0.035);
   s_Top6->GetYaxis()->SetTitleSize(0.035);
   s_Top6->GetYaxis()->SetTitleFont(42);
   s_Top6->GetZaxis()->SetLabelFont(42);
   s_Top6->GetZaxis()->SetLabelSize(0.035);
   s_Top6->GetZaxis()->SetTitleSize(0.035);
   s_Top6->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(s_Top,"");
   
   TH1F *VVLF7 = new TH1F("VVLF7","VVLF",11,0.2,1);
   VVLF7->SetBinContent(1,7.038677);
   VVLF7->SetBinContent(2,3.879137);
   VVLF7->SetBinContent(3,4.896292);
   VVLF7->SetBinContent(4,3.888224);
   VVLF7->SetBinContent(5,0.4619137);
   VVLF7->SetBinContent(6,1.066361);
   VVLF7->SetBinContent(7,0.2107346);
   VVLF7->SetBinContent(8,0.001184799);
   VVLF7->SetBinContent(9,0.001841913);
   VVLF7->SetBinContent(10,0.000598339);
   VVLF7->SetBinContent(11,2.132251e-08);
   VVLF7->SetBinError(1,3.04987);
   VVLF7->SetBinError(2,2.995479);
   VVLF7->SetBinError(3,2.277104);
   VVLF7->SetBinError(4,1.790556);
   VVLF7->SetBinError(5,0.2519933);
   VVLF7->SetBinError(6,1.039733);
   VVLF7->SetBinError(7,0.1759718);
   VVLF7->SetBinError(8,0.1246651);
   VVLF7->SetBinError(9,0.08275744);
   VVLF7->SetBinError(10,0.04196766);
   VVLF7->SetEntries(11);
   VVLF7->SetDirectory(0);

   ci = TColor::GetColor("#666666");
   VVLF7->SetFillColor(ci);
   VVLF7->GetXaxis()->SetLabelFont(42);
   VVLF7->GetXaxis()->SetLabelSize(0.035);
   VVLF7->GetXaxis()->SetTitleSize(0.035);
   VVLF7->GetXaxis()->SetTitleFont(42);
   VVLF7->GetYaxis()->SetLabelFont(42);
   VVLF7->GetYaxis()->SetLabelSize(0.035);
   VVLF7->GetYaxis()->SetTitleSize(0.035);
   VVLF7->GetYaxis()->SetTitleFont(42);
   VVLF7->GetZaxis()->SetLabelFont(42);
   VVLF7->GetZaxis()->SetLabelSize(0.035);
   VVLF7->GetZaxis()->SetTitleSize(0.035);
   VVLF7->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(VVLF,"");
   
   TH1F *TT8 = new TH1F("TT8","TT",11,0.2,1);
   TT8->SetBinContent(1,1235.787);
   TT8->SetBinContent(2,858.1849);
   TT8->SetBinContent(3,544.6453);
   TT8->SetBinContent(4,268.4228);
   TT8->SetBinContent(5,74.15147);
   TT8->SetBinContent(6,42.389);
   TT8->SetBinContent(7,23.74077);
   TT8->SetBinContent(8,9.451703);
   TT8->SetBinContent(9,3.240477);
   TT8->SetBinContent(10,0.2992829);
   TT8->SetBinContent(11,3.060313e-06);
   TT8->SetBinError(1,23.70311);
   TT8->SetBinError(2,19.52883);
   TT8->SetBinError(3,15.5354);
   TT8->SetBinError(4,11.06919);
   TT8->SetBinError(5,5.582406);
   TT8->SetBinError(6,4.543709);
   TT8->SetBinError(7,3.148086);
   TT8->SetBinError(8,1.915351);
   TT8->SetBinError(9,1.290115);
   TT8->SetBinError(10,0.385989);
   TT8->SetEntries(11);
   TT8->SetDirectory(0);

   ci = TColor::GetColor("#3333ff");
   TT8->SetFillColor(ci);
   TT8->GetXaxis()->SetLabelFont(42);
   TT8->GetXaxis()->SetLabelSize(0.035);
   TT8->GetXaxis()->SetTitleSize(0.035);
   TT8->GetXaxis()->SetTitleFont(42);
   TT8->GetYaxis()->SetLabelFont(42);
   TT8->GetYaxis()->SetLabelSize(0.035);
   TT8->GetYaxis()->SetTitleSize(0.035);
   TT8->GetYaxis()->SetTitleFont(42);
   TT8->GetZaxis()->SetLabelFont(42);
   TT8->GetZaxis()->SetLabelSize(0.035);
   TT8->GetZaxis()->SetTitleSize(0.035);
   TT8->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(TT,"");
   
   TH1F *Zj0b9 = new TH1F("Zj0b9","Zj0b",11,0.2,1);
   Zj0b9->SetBinContent(1,5.746664);
   Zj0b9->SetBinContent(2,1.364853);
   Zj0b9->SetBinContent(3,5.111022);
   Zj0b9->SetBinContent(4,1.727827);
   Zj0b9->SetBinContent(5,0.01475042);
   Zj0b9->SetBinContent(6,0.04029874);
   Zj0b9->SetBinContent(7,1.400541e-08);
   Zj0b9->SetBinContent(8,1.400541e-08);
   Zj0b9->SetBinContent(9,1.400541e-08);
   Zj0b9->SetBinContent(10,1.400541e-08);
   Zj0b9->SetBinContent(11,1.400541e-08);
   Zj0b9->SetBinError(1,3.427241);
   Zj0b9->SetBinError(2,1.342277);
   Zj0b9->SetBinError(3,2.991541);
   Zj0b9->SetBinError(4,1.679403);
   Zj0b9->SetBinError(5,0.01517587);
   Zj0b9->SetBinError(6,0.02091376);
   Zj0b9->SetEntries(11);
   Zj0b9->SetDirectory(0);

   ci = TColor::GetColor("#cccc00");
   Zj0b9->SetFillColor(ci);
   Zj0b9->GetXaxis()->SetLabelFont(42);
   Zj0b9->GetXaxis()->SetLabelSize(0.035);
   Zj0b9->GetXaxis()->SetTitleSize(0.035);
   Zj0b9->GetXaxis()->SetTitleFont(42);
   Zj0b9->GetYaxis()->SetLabelFont(42);
   Zj0b9->GetYaxis()->SetLabelSize(0.035);
   Zj0b9->GetYaxis()->SetTitleSize(0.035);
   Zj0b9->GetYaxis()->SetTitleFont(42);
   Zj0b9->GetZaxis()->SetLabelFont(42);
   Zj0b9->GetZaxis()->SetLabelSize(0.035);
   Zj0b9->GetZaxis()->SetTitleSize(0.035);
   Zj0b9->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Zj0b,"");
   
   TH1F *Zj1b10 = new TH1F("Zj1b10","Zj1b",11,0.2,1);
   Zj1b10->SetBinContent(1,16.30553);
   Zj1b10->SetBinContent(2,18.64535);
   Zj1b10->SetBinContent(3,3.174422);
   Zj1b10->SetBinContent(4,2.683328);
   Zj1b10->SetBinContent(5,0.02079204);
   Zj1b10->SetBinContent(6,0.03559701);
   Zj1b10->SetBinContent(7,4.092075e-08);
   Zj1b10->SetBinContent(8,0.04196167);
   Zj1b10->SetBinContent(9,0.01377165);
   Zj1b10->SetBinContent(10,4.092075e-08);
   Zj1b10->SetBinContent(11,4.092075e-08);
   Zj1b10->SetBinError(1,5.8352);
   Zj1b10->SetBinError(2,6.108608);
   Zj1b10->SetBinError(3,1.963317);
   Zj1b10->SetBinError(4,1.990104);
   Zj1b10->SetBinError(5,0.01658254);
   Zj1b10->SetBinError(6,0.02127779);
   Zj1b10->SetBinError(8,0.03212863);
   Zj1b10->SetBinError(9,0.01396441);
   Zj1b10->SetEntries(11);
   Zj1b10->SetDirectory(0);
   Zj1b10->SetFillColor(41);
   Zj1b10->GetXaxis()->SetLabelFont(42);
   Zj1b10->GetXaxis()->SetLabelSize(0.035);
   Zj1b10->GetXaxis()->SetTitleSize(0.035);
   Zj1b10->GetXaxis()->SetTitleFont(42);
   Zj1b10->GetYaxis()->SetLabelFont(42);
   Zj1b10->GetYaxis()->SetLabelSize(0.035);
   Zj1b10->GetYaxis()->SetTitleSize(0.035);
   Zj1b10->GetYaxis()->SetTitleFont(42);
   Zj1b10->GetZaxis()->SetLabelFont(42);
   Zj1b10->GetZaxis()->SetLabelSize(0.035);
   Zj1b10->GetZaxis()->SetTitleSize(0.035);
   Zj1b10->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Zj1b,"");
   
   TH1F *Zj2b11 = new TH1F("Zj2b11","Zj2b",11,0.2,1);
   Zj2b11->SetBinContent(1,28.07135);
   Zj2b11->SetBinContent(2,9.025328);
   Zj2b11->SetBinContent(3,21.9893);
   Zj2b11->SetBinContent(4,7.501509);
   Zj2b11->SetBinContent(5,0.06423886);
   Zj2b11->SetBinContent(6,4.059013);
   Zj2b11->SetBinContent(7,3.40404);
   Zj2b11->SetBinContent(8,6.514063);
   Zj2b11->SetBinContent(9,8.062884e-08);
   Zj2b11->SetBinContent(10,8.062884e-08);
   Zj2b11->SetBinContent(11,8.062884e-08);
   Zj2b11->SetBinError(1,7.436428);
   Zj2b11->SetBinError(2,3.760329);
   Zj2b11->SetBinError(3,6.433403);
   Zj2b11->SetBinError(4,3.596968);
   Zj2b11->SetBinError(5,0.02940703);
   Zj2b11->SetBinError(6,2.543493);
   Zj2b11->SetBinError(7,2.234334);
   Zj2b11->SetBinError(8,3.368336);
   Zj2b11->SetEntries(11);
   Zj2b11->SetDirectory(0);
   Zj2b11->SetFillColor(5);
   Zj2b11->GetXaxis()->SetLabelFont(42);
   Zj2b11->GetXaxis()->SetLabelSize(0.035);
   Zj2b11->GetXaxis()->SetTitleSize(0.035);
   Zj2b11->GetXaxis()->SetTitleFont(42);
   Zj2b11->GetYaxis()->SetLabelFont(42);
   Zj2b11->GetYaxis()->SetLabelSize(0.035);
   Zj2b11->GetYaxis()->SetTitleSize(0.035);
   Zj2b11->GetYaxis()->SetTitleFont(42);
   Zj2b11->GetZaxis()->SetLabelFont(42);
   Zj2b11->GetZaxis()->SetLabelSize(0.035);
   Zj2b11->GetZaxis()->SetTitleSize(0.035);
   Zj2b11->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(Zj2b,"");
   
   TH1F *VVHF12 = new TH1F("VVHF12","VVHF",11,0.2,1);
   VVHF12->SetBinContent(1,27.59053);
   VVHF12->SetBinContent(2,31.71415);
   VVHF12->SetBinContent(3,30.14149);
   VVHF12->SetBinContent(4,29.255);
   VVHF12->SetBinContent(5,14.25152);
   VVHF12->SetBinContent(6,11.63706);
   VVHF12->SetBinContent(7,11.60919);
   VVHF12->SetBinContent(8,7.737504);
   VVHF12->SetBinContent(9,3.863146);
   VVHF12->SetBinContent(10,1.45831);
   VVHF12->SetBinContent(11,0.2943473);
   VVHF12->SetBinError(1,1.656118);
   VVHF12->SetBinError(2,1.767414);
   VVHF12->SetBinError(3,1.757628);
   VVHF12->SetBinError(4,1.669167);
   VVHF12->SetBinError(5,1.125079);
   VVHF12->SetBinError(6,1.034673);
   VVHF12->SetBinError(7,1.004998);
   VVHF12->SetBinError(8,0.8398987);
   VVHF12->SetBinError(9,0.6468376);
   VVHF12->SetBinError(10,0.4110365);
   VVHF12->SetBinError(11,0.1336276);
   VVHF12->SetEntries(11);
   VVHF12->SetDirectory(0);

   ci = TColor::GetColor("#cccccc");
   VVHF12->SetFillColor(ci);
   VVHF12->GetXaxis()->SetLabelFont(42);
   VVHF12->GetXaxis()->SetLabelSize(0.035);
   VVHF12->GetXaxis()->SetTitleSize(0.035);
   VVHF12->GetXaxis()->SetTitleFont(42);
   VVHF12->GetYaxis()->SetLabelFont(42);
   VVHF12->GetYaxis()->SetLabelSize(0.035);
   VVHF12->GetYaxis()->SetTitleSize(0.035);
   VVHF12->GetYaxis()->SetTitleFont(42);
   VVHF12->GetZaxis()->SetLabelFont(42);
   VVHF12->GetZaxis()->SetLabelSize(0.035);
   VVHF12->GetZaxis()->SetTitleSize(0.035);
   VVHF12->GetZaxis()->SetTitleFont(42);
   gg_plus_ZH125_high_Zpt->Add(VVHF,"");
   gg_plus_ZH125_high_Zpt->Draw("hist");
   
   Double_t Graph_from_VVHF_fx1001[11] = {
   0.2363636,
   0.3090909,
   0.3818182,
   0.4545455,
   0.5272727,
   0.6,
   0.6727273,
   0.7454545,
   0.8181818,
   0.8909091,
   0.9636364};
   Double_t Graph_from_VVHF_fy1001[11] = {
   2107.448,
   1611.938,
   1101.789,
   625.9399,
   185.8509,
   143.2936,
   97.3751,
   52.62502,
   19.67903,
   5.156955,
   0.460324};
   Double_t Graph_from_VVHF_fex1001[11] = {
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364};
   Double_t Graph_from_VVHF_fey1001[11] = {
   30.79103,
   26.98326,
   21.28412,
   15.41898,
   7.351214,
   6.665414,
   5.67607,
   4.207673,
   1.620611,
   0.7277215,
   0.1402287};
   TGraphErrors *gre = new TGraphErrors(11,Graph_from_VVHF_fx1001,Graph_from_VVHF_fy1001,Graph_from_VVHF_fex1001,Graph_from_VVHF_fey1001);
   gre->SetName("Graph_from_VVHF");
   gre->SetTitle("VVHF");

   ci = TColor::GetColor("#333333");
   gre->SetFillColor(ci);
   gre->SetFillStyle(3013);
   
   TH1F *Graph_Graph_from_VVHF1001 = new TH1F("Graph_Graph_from_VVHF1001","VVHF",100,0.12,1.08);
   Graph_Graph_from_VVHF1001->SetMinimum(0.2880858);
   Graph_Graph_from_VVHF1001->SetMaximum(2352.031);
   Graph_Graph_from_VVHF1001->SetDirectory(0);
   Graph_Graph_from_VVHF1001->SetStats(0);
   Graph_Graph_from_VVHF1001->SetFillColor(63);
   Graph_Graph_from_VVHF1001->SetLineStyle(0);
   Graph_Graph_from_VVHF1001->SetMarkerStyle(20);
   Graph_Graph_from_VVHF1001->SetMarkerSize(1.2);
   Graph_Graph_from_VVHF1001->GetXaxis()->SetLabelFont(42);
   Graph_Graph_from_VVHF1001->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_VVHF1001->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_from_VVHF1001->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_from_VVHF1001->GetXaxis()->SetTitleFont(42);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetLabelFont(42);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_from_VVHF1001->GetYaxis()->SetTitleFont(42);
   Graph_Graph_from_VVHF1001->GetZaxis()->SetLabelFont(42);
   Graph_Graph_from_VVHF1001->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_VVHF1001->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_from_VVHF1001->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_from_VVHF1001->GetZaxis()->SetTitleFont(42);
   gre->SetHistogram(Graph_Graph_from_VVHF1001);
   
   gre->Draw("2");
   
   TH1F *noData13 = new TH1F("noData13","noData",11,0.2,1);
   noData13->SetBinContent(0,27231);
   noData13->SetBinContent(1,2096);
   noData13->SetBinContent(2,1625);
   noData13->SetBinContent(3,1128);
   noData13->SetBinContent(4,638);
   noData13->SetBinContent(5,186);
   noData13->SetBinContent(6,129);
   noData13->SetBinContent(7,92);
   noData13->SetBinContent(8,57);
   noData13->SetBinContent(9,25);
   noData13->SetBinContent(10,3);
   noData13->SetEntries(33210);
   noData13->SetDirectory(0);
   noData13->SetFillColor(63);
   noData13->SetLineStyle(0);
   noData13->SetMarkerStyle(20);
   noData13->SetMarkerSize(1.2);
   noData13->GetXaxis()->SetLabelFont(42);
   noData13->GetXaxis()->SetLabelOffset(0.007);
   noData13->GetXaxis()->SetLabelSize(0.05);
   noData13->GetXaxis()->SetTitleSize(0.05);
   noData13->GetXaxis()->SetTitleFont(42);
   noData13->GetYaxis()->SetLabelFont(42);
   noData13->GetYaxis()->SetLabelOffset(0.007);
   noData13->GetYaxis()->SetLabelSize(0.05);
   noData13->GetYaxis()->SetTitleSize(0.05);
   noData13->GetYaxis()->SetTitleOffset(1.4);
   noData13->GetYaxis()->SetTitleFont(42);
   noData13->GetZaxis()->SetLabelFont(42);
   noData13->GetZaxis()->SetLabelOffset(0.007);
   noData13->GetZaxis()->SetLabelSize(0.05);
   noData13->GetZaxis()->SetTitleSize(0.05);
   noData13->GetZaxis()->SetTitleFont(42);
   noData13->Draw("E,same");
   
   TLegend *leg = new TLegend(0.45,0.6,0.75,0.92,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.035);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(2);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   TLegendEntry *entry=leg->AddEntry("noData","Data","P");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   entry=leg->AddEntry("VVHF","VVHF","F");

   ci = TColor::GetColor("#cccccc");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Zj2b","Z + b#bar{b}","F");
   entry->SetFillColor(5);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Zj1b","Z + b","F");
   entry->SetFillColor(41);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Zj0b","Z+udscg","F");

   ci = TColor::GetColor("#cccc00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("TT","t#bar{t}","F");

   ci = TColor::GetColor("#3333ff");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("VVLF","VVLF","F");

   ci = TColor::GetColor("#666666");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   leg->Draw();
   
   leg = new TLegend(0.68,0.6,0.92,0.92,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.035);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(2);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   entry=leg->AddEntry("s_Top","Single top","F");

   ci = TColor::GetColor("#00ffcc");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Wj0b","W+udscg","F");

   ci = TColor::GetColor("#009900");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Wj1b","W + b","F");

   ci = TColor::GetColor("#66cc66");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("ZH_hbb","ZH(b#bar{b}) 125","F");
   entry->SetFillColor(2);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("WH_hbb","WH(b#bar{b}) 125","F");
   entry->SetFillColor(2);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Wj2b","W + b#bar{b}","F");

   ci = TColor::GetColor("#00ff00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Graph_from_VVHF","MC uncert. (stat.)","fl");

   ci = TColor::GetColor("#333333");
   entry->SetFillColor(ci);
   entry->SetFillStyle(3013);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   leg->Draw();
   TLatex *   tex = new TLatex(0.17,0.88,"CMS Preliminary");
tex->SetNDC();
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.17,0.83,"#sqrt{s} =  13TeV, L = 35.9 fb^{-1}");
tex->SetNDC();
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.17,0.78,"1-lep (#mu)");
tex->SetNDC();
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
   oben->Modified();
   gg_plus_ZH125_high_Zpt->cd();
  
// ------------>Primitives in pad: unten
   TPad *unten = new TPad("unten", "unten",0,0,1,0.29);
   unten->Draw();
   unten->cd();
   unten->Range(0.07317074,-3.084615,1.04878,2.9);
   unten->SetFillColor(0);
   unten->SetFillStyle(4000);
   unten->SetBorderMode(0);
   unten->SetBorderSize(2);
   unten->SetTickx(1);
   unten->SetTicky(1);
   unten->SetLeftMargin(0.13);
   unten->SetRightMargin(0.05);
   unten->SetTopMargin(0);
   unten->SetBottomMargin(0.35);
   unten->SetFrameFillStyle(1000);
   unten->SetFrameBorderMode(0);
   unten->SetFrameFillStyle(1000);
   unten->SetFrameBorderMode(0);
   Double_t xAxis1[12] = {0.2, 0.2727273, 0.3454545, 0.4181818, 0.4909091, 0.5636364, 0.6363636, 0.7090909, 0.7818182, 0.8545455, 0.9272727, 1}; 
   
   TH1F *Ratio14 = new TH1F("Ratio14","",11, xAxis1);
   Ratio14->SetBinContent(1,0.9945676);
   Ratio14->SetBinContent(2,1.008103);
   Ratio14->SetBinContent(3,1.023789);
   Ratio14->SetBinContent(4,1.019267);
   Ratio14->SetBinContent(5,1.000802);
   Ratio14->SetBinContent(6,0.9002495);
   Ratio14->SetBinContent(7,0.9448001);
   Ratio14->SetBinContent(8,1.083135);
   Ratio14->SetBinContent(9,1.270388);
   Ratio14->SetBinContent(10,0.5817387);
   Ratio14->SetBinContent(11,0.0001);
   Ratio14->SetBinError(1,0.02172394);
   Ratio14->SetBinError(2,0.02500796);
   Ratio14->SetBinError(3,0.03048289);
   Ratio14->SetBinError(4,0.04035317);
   Ratio14->SetBinError(5,0.07338237);
   Ratio14->SetBinError(6,0.07926255);
   Ratio14->SetBinError(7,0.09850222);
   Ratio14->SetBinError(8,0.1434647);
   Ratio14->SetBinError(9,0.2540775);
   Ratio14->SetBinError(10,0.335867);
   Ratio14->SetBinError(11,3.910289);
   Ratio14->SetMinimum(-0.99);
   Ratio14->SetMaximum(2.9);
   Ratio14->SetEntries(12);
   Ratio14->SetDirectory(0);
   Ratio14->SetStats(0);
   Ratio14->SetFillColor(63);
   Ratio14->SetLineStyle(0);
   Ratio14->SetMarkerStyle(20);
   Ratio14->GetXaxis()->SetTitle("BDT Output");
   Ratio14->GetXaxis()->SetRange(1,11);
   Ratio14->GetXaxis()->SetLabelFont(42);
   Ratio14->GetXaxis()->SetLabelOffset(0.03);
   Ratio14->GetXaxis()->SetLabelSize(0.09);
   Ratio14->GetXaxis()->SetTitleSize(0.11);
   Ratio14->GetXaxis()->SetTitleFont(42);
   Ratio14->GetYaxis()->SetTitle("Data/MC");
   Ratio14->GetYaxis()->CenterTitle(true);
   Ratio14->GetYaxis()->SetNdivisions(505);
   Ratio14->GetYaxis()->SetLabelFont(22);
   Ratio14->GetYaxis()->SetLabelOffset(0.007);
   Ratio14->GetYaxis()->SetLabelSize(0.07);
   Ratio14->GetYaxis()->SetTitleSize(0.11);
   Ratio14->GetYaxis()->SetTitleOffset(0.4);
   Ratio14->GetYaxis()->SetTitleFont(22);
   Ratio14->GetZaxis()->SetLabelFont(42);
   Ratio14->GetZaxis()->SetLabelOffset(0.007);
   Ratio14->GetZaxis()->SetLabelSize(0.05);
   Ratio14->GetZaxis()->SetTitleSize(0.05);
   Ratio14->GetZaxis()->SetTitleFont(42);
   Ratio14->Draw("E1");
   
   Double_t Graph_from_WH_hbb_postfit_fx3001[11] = {
   0.2363636,
   0.3090909,
   0.3818182,
   0.4545455,
   0.5272727,
   0.6,
   0.6727273,
   0.7454545,
   0.8181818,
   0.8909091,
   0.9636364};
   Double_t Graph_from_WH_hbb_postfit_fy3001[11] = {
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1};
   Double_t Graph_from_WH_hbb_postfit_felx3001[11] = {
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364};
   Double_t Graph_from_WH_hbb_postfit_fely3001[11] = {
   0.0363432,
   0.04167682,
   0.04800012,
   0.05773774,
   0.09265006,
   0.1024577,
   0.1222634,
   0.1658587,
   0.17606,
   0.274881,
   0.6558824};
   Double_t Graph_from_WH_hbb_postfit_fehx3001[11] = {
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364};
   Double_t Graph_from_WH_hbb_postfit_fehy3001[11] = {
   0.0363432,
   0.04167682,
   0.04800012,
   0.05773774,
   0.09265006,
   0.1024577,
   0.1222634,
   0.1658587,
   0.17606,
   0.274881,
   0.6558824};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(11,Graph_from_WH_hbb_postfit_fx3001,Graph_from_WH_hbb_postfit_fy3001,Graph_from_WH_hbb_postfit_felx3001,Graph_from_WH_hbb_postfit_fehx3001,Graph_from_WH_hbb_postfit_fely3001,Graph_from_WH_hbb_postfit_fehy3001);
   grae->SetName("Graph_from_WH_hbb_postfit");
   grae->SetTitle("WH_hbb_postfit");
   grae->SetFillColor(5);
   grae->SetFillStyle(3001);
   
   TH1F *Graph_Graph_from_WH_hbb_postfit3001 = new TH1F("Graph_Graph_from_WH_hbb_postfit3001","WH_hbb_postfit",100,0.12,1.08);
   Graph_Graph_from_WH_hbb_postfit3001->SetMinimum(0.2129412);
   Graph_Graph_from_WH_hbb_postfit3001->SetMaximum(1.787059);
   Graph_Graph_from_WH_hbb_postfit3001->SetDirectory(0);
   Graph_Graph_from_WH_hbb_postfit3001->SetStats(0);
   Graph_Graph_from_WH_hbb_postfit3001->SetFillColor(63);
   Graph_Graph_from_WH_hbb_postfit3001->SetLineStyle(0);
   Graph_Graph_from_WH_hbb_postfit3001->SetMarkerStyle(20);
   Graph_Graph_from_WH_hbb_postfit3001->SetMarkerSize(1.2);
   Graph_Graph_from_WH_hbb_postfit3001->GetXaxis()->SetLabelFont(42);
   Graph_Graph_from_WH_hbb_postfit3001->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_WH_hbb_postfit3001->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetXaxis()->SetTitleFont(42);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetLabelFont(42);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_from_WH_hbb_postfit3001->GetYaxis()->SetTitleFont(42);
   Graph_Graph_from_WH_hbb_postfit3001->GetZaxis()->SetLabelFont(42);
   Graph_Graph_from_WH_hbb_postfit3001->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_WH_hbb_postfit3001->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_from_WH_hbb_postfit3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph_from_WH_hbb_postfit3001);
   
   grae->Draw("2");
   
   Double_t Graph_from_RefError_fx1002[11] = {
   0.2363636,
   0.3090909,
   0.3818182,
   0.4545455,
   0.5272727,
   0.6,
   0.6727273,
   0.7454545,
   0.8181818,
   0.8909091,
   0.9636364};
   Double_t Graph_from_RefError_fy1002[11] = {
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1};
   Double_t Graph_from_RefError_fex1002[11] = {
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364,
   0.03636364};
   Double_t Graph_from_RefError_fey1002[11] = {
   0.01461057,
   0.01673964,
   0.01931778,
   0.02463333,
   0.03955436,
   0.04651578,
   0.05829078,
   0.07995576,
   0.08235215,
   0.1411146,
   0.3046304};
   gre = new TGraphErrors(11,Graph_from_RefError_fx1002,Graph_from_RefError_fy1002,Graph_from_RefError_fex1002,Graph_from_RefError_fey1002);
   gre->SetName("Graph_from_RefError");
   gre->SetTitle("noData");

   ci = TColor::GetColor("#333333");
   gre->SetFillColor(ci);
   gre->SetFillStyle(3013);
   gre->SetLineStyle(0);
   gre->SetMarkerStyle(20);
   
   TH1F *Graph_Graph_from_RefError1002 = new TH1F("Graph_Graph_from_RefError1002","noData",100,0.12,1.08);
   Graph_Graph_from_RefError1002->SetMinimum(0.6344435);
   Graph_Graph_from_RefError1002->SetMaximum(1.365557);
   Graph_Graph_from_RefError1002->SetDirectory(0);
   Graph_Graph_from_RefError1002->SetStats(0);
   Graph_Graph_from_RefError1002->SetFillColor(63);
   Graph_Graph_from_RefError1002->SetLineStyle(0);
   Graph_Graph_from_RefError1002->SetMarkerStyle(20);
   Graph_Graph_from_RefError1002->SetMarkerSize(1.2);
   Graph_Graph_from_RefError1002->GetXaxis()->SetLabelFont(42);
   Graph_Graph_from_RefError1002->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_RefError1002->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_from_RefError1002->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_from_RefError1002->GetXaxis()->SetTitleFont(42);
   Graph_Graph_from_RefError1002->GetYaxis()->SetLabelFont(42);
   Graph_Graph_from_RefError1002->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_RefError1002->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_from_RefError1002->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_from_RefError1002->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_from_RefError1002->GetYaxis()->SetTitleFont(42);
   Graph_Graph_from_RefError1002->GetZaxis()->SetLabelFont(42);
   Graph_Graph_from_RefError1002->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph_from_RefError1002->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_from_RefError1002->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_from_RefError1002->GetZaxis()->SetTitleFont(42);
   gre->SetHistogram(Graph_Graph_from_RefError1002);
   
   gre->Draw("2");
   Double_t xAxis2[12] = {0.2, 0.2727273, 0.3454545, 0.4181818, 0.4909091, 0.5636364, 0.6363636, 0.7090909, 0.7818182, 0.8545455, 0.9272727, 1}; 
   
   TH1F *Ratio15 = new TH1F("Ratio15","",11, xAxis2);
   Ratio15->SetBinContent(1,0.9945676);
   Ratio15->SetBinContent(2,1.008103);
   Ratio15->SetBinContent(3,1.023789);
   Ratio15->SetBinContent(4,1.019267);
   Ratio15->SetBinContent(5,1.000802);
   Ratio15->SetBinContent(6,0.9002495);
   Ratio15->SetBinContent(7,0.9448001);
   Ratio15->SetBinContent(8,1.083135);
   Ratio15->SetBinContent(9,1.270388);
   Ratio15->SetBinContent(10,0.5817387);
   Ratio15->SetBinContent(11,0.0001);
   Ratio15->SetBinError(1,0.02172394);
   Ratio15->SetBinError(2,0.02500796);
   Ratio15->SetBinError(3,0.03048289);
   Ratio15->SetBinError(4,0.04035317);
   Ratio15->SetBinError(5,0.07338237);
   Ratio15->SetBinError(6,0.07926255);
   Ratio15->SetBinError(7,0.09850222);
   Ratio15->SetBinError(8,0.1434647);
   Ratio15->SetBinError(9,0.2540775);
   Ratio15->SetBinError(10,0.335867);
   Ratio15->SetBinError(11,3.910289);
   Ratio15->SetMinimum(-0.99);
   Ratio15->SetMaximum(2.9);
   Ratio15->SetEntries(12);
   Ratio15->SetDirectory(0);
   Ratio15->SetStats(0);
   Ratio15->SetFillColor(63);
   Ratio15->SetLineStyle(0);
   Ratio15->SetMarkerStyle(20);
   Ratio15->GetXaxis()->SetTitle("BDT Output");
   Ratio15->GetXaxis()->SetRange(1,11);
   Ratio15->GetXaxis()->SetLabelFont(42);
   Ratio15->GetXaxis()->SetLabelOffset(0.03);
   Ratio15->GetXaxis()->SetLabelSize(0.09);
   Ratio15->GetXaxis()->SetTitleSize(0.11);
   Ratio15->GetXaxis()->SetTitleFont(42);
   Ratio15->GetYaxis()->SetTitle("Data/MC");
   Ratio15->GetYaxis()->CenterTitle(true);
   Ratio15->GetYaxis()->SetNdivisions(505);
   Ratio15->GetYaxis()->SetLabelFont(22);
   Ratio15->GetYaxis()->SetLabelOffset(0.007);
   Ratio15->GetYaxis()->SetLabelSize(0.07);
   Ratio15->GetYaxis()->SetTitleSize(0.11);
   Ratio15->GetYaxis()->SetTitleOffset(0.4);
   Ratio15->GetYaxis()->SetTitleFont(22);
   Ratio15->GetZaxis()->SetLabelFont(42);
   Ratio15->GetZaxis()->SetLabelOffset(0.007);
   Ratio15->GetZaxis()->SetLabelSize(0.05);
   Ratio15->GetZaxis()->SetTitleSize(0.05);
   Ratio15->GetZaxis()->SetTitleFont(42);
   Ratio15->Draw("E1SAME");
   
   leg = new TLegend(0.3,0.85,0.93,0.97,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.075);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(2);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   entry=leg->AddEntry("Graph_from_WH_hbb_postfit","MC(stat.+Postfit syst.)","f");
   entry->SetFillColor(5);
   entry->SetFillStyle(3001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("Graph_from_RefError","MC(stat.)","f");

   ci = TColor::GetColor("#333333");
   entry->SetFillColor(ci);
   entry->SetFillStyle(3013);
   entry->SetLineColor(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   leg->Draw();
   TLine *line = new TLine(0.2,1,1,1);
   line->Draw();
   unten->Modified();
   gg_plus_ZH125_high_Zpt->cd();
   gg_plus_ZH125_high_Zpt->Modified();
   gg_plus_ZH125_high_Zpt->cd();
   gg_plus_ZH125_high_Zpt->SetSelected(gg_plus_ZH125_high_Zpt);
}
