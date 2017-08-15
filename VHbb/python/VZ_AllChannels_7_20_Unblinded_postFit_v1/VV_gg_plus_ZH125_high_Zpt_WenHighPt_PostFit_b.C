void VV_gg_plus_ZH125_high_Zpt_WenHighPt_PostFit_b()
{
//=========Macro generated from canvas: gg_plus_ZH125_high_Zpt/
//=========  (Sat Jul 22 20:26:16 2017) by ROOT version6.02/05
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
   oben->Range(0.07317074,-1.700269,1.04878,7.927313);
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
   gg_plus_ZH125_high_Zpt->SetMaximum(1.071423e+07);
   
   TH1F *gg_plus_ZH125_high_Zpt_stack_1 = new TH1F("gg_plus_ZH125_high_Zpt_stack_1","",11,0.2,1);
   gg_plus_ZH125_high_Zpt_stack_1->SetMinimum(0.01994026);
   gg_plus_ZH125_high_Zpt_stack_1->SetMaximum(2.79212e+07);
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
   Wj2b1->SetBinContent(1,127.6735);
   Wj2b1->SetBinContent(2,118.2825);
   Wj2b1->SetBinContent(3,108.4275);
   Wj2b1->SetBinContent(4,79.06245);
   Wj2b1->SetBinContent(5,32.66254);
   Wj2b1->SetBinContent(6,28.91598);
   Wj2b1->SetBinContent(7,23.5457);
   Wj2b1->SetBinContent(8,15.82188);
   Wj2b1->SetBinContent(9,6.69216);
   Wj2b1->SetBinContent(10,1.786647);
   Wj2b1->SetBinContent(11,0.1970039);
   Wj2b1->SetBinError(1,4.054247);
   Wj2b1->SetBinError(2,3.849818);
   Wj2b1->SetBinError(3,3.947286);
   Wj2b1->SetBinError(4,2.90831);
   Wj2b1->SetBinError(5,1.60589);
   Wj2b1->SetBinError(6,2.370407);
   Wj2b1->SetBinError(7,1.070579);
   Wj2b1->SetBinError(8,0.7868253);
   Wj2b1->SetBinError(9,0.3986132);
   Wj2b1->SetBinError(10,0.1600168);
   Wj2b1->SetBinError(11,0.05441163);
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
   WH_hbb2->SetBinContent(1,4.6246);
   WH_hbb2->SetBinContent(2,3.964391);
   WH_hbb2->SetBinContent(3,3.310712);
   WH_hbb2->SetBinContent(4,2.644363);
   WH_hbb2->SetBinContent(5,0.9334819);
   WH_hbb2->SetBinContent(6,0.788821);
   WH_hbb2->SetBinContent(7,0.6322587);
   WH_hbb2->SetBinContent(8,0.437712);
   WH_hbb2->SetBinContent(9,0.2025138);
   WH_hbb2->SetBinContent(10,0.04888018);
   WH_hbb2->SetBinContent(11,1.758773e-08);
   WH_hbb2->SetBinError(1,0.1292294);
   WH_hbb2->SetBinError(2,0.1208997);
   WH_hbb2->SetBinError(3,0.107283);
   WH_hbb2->SetBinError(4,0.09764115);
   WH_hbb2->SetBinError(5,0.0591073);
   WH_hbb2->SetBinError(6,0.05106212);
   WH_hbb2->SetBinError(7,0.04795514);
   WH_hbb2->SetBinError(8,0.03663873);
   WH_hbb2->SetBinError(9,0.02448674);
   WH_hbb2->SetBinError(10,0.01511705);
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
   ZH_hbb3->SetBinContent(1,0.1695072);
   ZH_hbb3->SetBinContent(2,0.127427);
   ZH_hbb3->SetBinContent(3,0.09230535);
   ZH_hbb3->SetBinContent(4,0.08222871);
   ZH_hbb3->SetBinContent(5,0.03802816);
   ZH_hbb3->SetBinContent(6,0.02081342);
   ZH_hbb3->SetBinContent(7,0.01175338);
   ZH_hbb3->SetBinContent(8,0.008768677);
   ZH_hbb3->SetBinContent(9,0.001303357);
   ZH_hbb3->SetBinContent(10,0.002197422);
   ZH_hbb3->SetBinContent(11,5.543326e-10);
   ZH_hbb3->SetBinError(1,0.01362943);
   ZH_hbb3->SetBinError(2,0.01176574);
   ZH_hbb3->SetBinError(3,0.01040266);
   ZH_hbb3->SetBinError(4,0.009570982);
   ZH_hbb3->SetBinError(5,0.005662681);
   ZH_hbb3->SetBinError(6,0.004262249);
   ZH_hbb3->SetBinError(7,0.003467105);
   ZH_hbb3->SetBinError(8,0.003345706);
   ZH_hbb3->SetBinError(9,0.0008487699);
   ZH_hbb3->SetBinError(10,0.001447753);
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
   Wj1b4->SetBinContent(1,89.91739);
   Wj1b4->SetBinContent(2,81.28138);
   Wj1b4->SetBinContent(3,54.71474);
   Wj1b4->SetBinContent(4,26.39528);
   Wj1b4->SetBinContent(5,10.26739);
   Wj1b4->SetBinContent(6,5.762223);
   Wj1b4->SetBinContent(7,3.590337);
   Wj1b4->SetBinContent(8,2.298631);
   Wj1b4->SetBinContent(9,1.422965);
   Wj1b4->SetBinContent(10,0.4442263);
   Wj1b4->SetBinContent(11,0.03020719);
   Wj1b4->SetBinError(1,2.907046);
   Wj1b4->SetBinError(2,3.101318);
   Wj1b4->SetBinError(3,2.665071);
   Wj1b4->SetBinError(4,1.333319);
   Wj1b4->SetBinError(5,0.8213128);
   Wj1b4->SetBinError(6,0.4769547);
   Wj1b4->SetBinError(7,0.3714796);
   Wj1b4->SetBinError(8,0.3613121);
   Wj1b4->SetBinError(9,0.165669);
   Wj1b4->SetBinError(10,0.1031243);
   Wj1b4->SetBinError(11,0.02055787);
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
   Wj0b5->SetBinContent(1,54.47439);
   Wj0b5->SetBinContent(2,42.43167);
   Wj0b5->SetBinContent(3,34.66966);
   Wj0b5->SetBinContent(4,19.69083);
   Wj0b5->SetBinContent(5,2.5203);
   Wj0b5->SetBinContent(6,11.04923);
   Wj0b5->SetBinContent(7,1.454987);
   Wj0b5->SetBinContent(8,0.0001057664);
   Wj0b5->SetBinContent(9,0.09262703);
   Wj0b5->SetBinContent(10,1.663838e-07);
   Wj0b5->SetBinContent(11,1.663838e-07);
   Wj0b5->SetBinError(1,8.235307);
   Wj0b5->SetBinError(2,7.47673);
   Wj0b5->SetBinError(3,6.763849);
   Wj0b5->SetBinError(4,5.075609);
   Wj0b5->SetBinError(5,1.447771);
   Wj0b5->SetBinError(6,3.402567);
   Wj0b5->SetBinError(7,1.037836);
   Wj0b5->SetBinError(8,9.747584e-05);
   Wj0b5->SetBinError(9,0.0825917);
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
   s_Top6->SetBinContent(1,251.3502);
   s_Top6->SetBinContent(2,179.9508);
   s_Top6->SetBinContent(3,137.322);
   s_Top6->SetBinContent(4,76.22221);
   s_Top6->SetBinContent(5,25.45879);
   s_Top6->SetBinContent(6,12.3729);
   s_Top6->SetBinContent(7,9.009881);
   s_Top6->SetBinContent(8,4.025795);
   s_Top6->SetBinContent(9,0.8062375);
   s_Top6->SetBinContent(10,0.365217);
   s_Top6->SetBinContent(11,6.968839e-07);
   s_Top6->SetBinError(1,7.064983);
   s_Top6->SetBinError(2,5.994725);
   s_Top6->SetBinError(3,5.379903);
   s_Top6->SetBinError(4,3.830852);
   s_Top6->SetBinError(5,2.168929);
   s_Top6->SetBinError(6,1.576439);
   s_Top6->SetBinError(7,1.278161);
   s_Top6->SetBinError(8,0.7477397);
   s_Top6->SetBinError(9,0.399692);
   s_Top6->SetBinError(10,0.3209269);
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
   VVLF7->SetBinContent(1,1.338038);
   VVLF7->SetBinContent(2,0.604131);
   VVLF7->SetBinContent(3,2.329753);
   VVLF7->SetBinContent(4,1.200557);
   VVLF7->SetBinContent(5,0.3197663);
   VVLF7->SetBinContent(6,0.04918687);
   VVLF7->SetBinContent(7,0.01232524);
   VVLF7->SetBinContent(8,0.0002111581);
   VVLF7->SetBinContent(9,0.0003184944);
   VVLF7->SetBinContent(10,0.01320425);
   VVLF7->SetBinContent(11,4.364596e-09);
   VVLF7->SetBinError(1,1.181751);
   VVLF7->SetBinError(2,2.735486);
   VVLF7->SetBinError(3,1.687629);
   VVLF7->SetBinError(4,1.279371);
   VVLF7->SetBinError(5,0.1961734);
   VVLF7->SetBinError(6,0.1440745);
   VVLF7->SetBinError(7,1.387902);
   VVLF7->SetBinError(8,0.09559883);
   VVLF7->SetBinError(9,0.05112141);
   VVLF7->SetBinError(10,0.01821796);
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
   TT8->SetBinContent(1,822.3085);
   TT8->SetBinContent(2,625.0109);
   TT8->SetBinContent(3,398.3085);
   TT8->SetBinContent(4,188.373);
   TT8->SetBinContent(5,49.0612);
   TT8->SetBinContent(6,30.23335);
   TT8->SetBinContent(7,20.87435);
   TT8->SetBinContent(8,6.716132);
   TT8->SetBinContent(9,1.995776);
   TT8->SetBinContent(10,0.08851245);
   TT8->SetBinContent(11,2.14297e-06);
   TT8->SetBinError(1,18.52271);
   TT8->SetBinError(2,15.85807);
   TT8->SetBinError(3,12.78639);
   TT8->SetBinError(4,8.857969);
   TT8->SetBinError(5,4.614909);
   TT8->SetBinError(6,3.242786);
   TT8->SetBinError(7,2.99896);
   TT8->SetBinError(8,1.766411);
   TT8->SetBinError(9,0.9597406);
   TT8->SetBinError(10,0.09991303);
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
   Zj0b9->SetBinContent(1,2.305258);
   Zj0b9->SetBinContent(2,1.887354);
   Zj0b9->SetBinContent(3,1.856421);
   Zj0b9->SetBinContent(4,6.04919e-09);
   Zj0b9->SetBinContent(5,0.0001581782);
   Zj0b9->SetBinContent(6,6.04919e-09);
   Zj0b9->SetBinContent(7,6.04919e-09);
   Zj0b9->SetBinContent(8,6.04919e-09);
   Zj0b9->SetBinContent(9,6.04919e-09);
   Zj0b9->SetBinContent(10,6.04919e-09);
   Zj0b9->SetBinContent(11,6.04919e-09);
   Zj0b9->SetBinError(1,2.267504);
   Zj0b9->SetBinError(2,1.912788);
   Zj0b9->SetBinError(3,1.948039);
   Zj0b9->SetBinError(5,0.0001628456);
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
   Zj1b10->SetBinContent(1,5.895399);
   Zj1b10->SetBinContent(2,5.603683);
   Zj1b10->SetBinContent(3,1.088708);
   Zj1b10->SetBinContent(4,1.315174);
   Zj1b10->SetBinContent(5,0.6204064);
   Zj1b10->SetBinContent(6,0.01427286);
   Zj1b10->SetBinContent(7,1.455128e-08);
   Zj1b10->SetBinContent(8,1.455128e-08);
   Zj1b10->SetBinContent(9,1.455128e-08);
   Zj1b10->SetBinContent(10,0.01363738);
   Zj1b10->SetBinContent(11,1.455128e-08);
   Zj1b10->SetBinError(1,2.986325);
   Zj1b10->SetBinError(2,3.092424);
   Zj1b10->SetBinError(3,1.118377);
   Zj1b10->SetBinError(4,1.252496);
   Zj1b10->SetBinError(5,0.6488292);
   Zj1b10->SetBinError(6,0.01236107);
   Zj1b10->SetBinError(10,0.01393493);
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
   Zj2b11->SetBinContent(1,15.12738);
   Zj2b11->SetBinContent(2,13.7742);
   Zj2b11->SetBinContent(3,8.401988);
   Zj2b11->SetBinContent(4,10.74991);
   Zj2b11->SetBinContent(5,3.037623);
   Zj2b11->SetBinContent(6,2.453421);
   Zj2b11->SetBinContent(7,4.007408);
   Zj2b11->SetBinContent(8,0.01230202);
   Zj2b11->SetBinContent(9,5.756423e-08);
   Zj2b11->SetBinContent(10,5.756423e-08);
   Zj2b11->SetBinContent(11,5.756423e-08);
   Zj2b11->SetBinError(1,5.044175);
   Zj2b11->SetBinError(2,4.848724);
   Zj2b11->SetBinError(3,3.679065);
   Zj2b11->SetBinError(4,4.319617);
   Zj2b11->SetBinError(5,3.580971);
   Zj2b11->SetBinError(6,1.959188);
   Zj2b11->SetBinError(7,2.78697);
   Zj2b11->SetBinError(8,0.0125036);
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
   VVHF12->SetBinContent(1,20.73283);
   VVHF12->SetBinContent(2,19.48166);
   VVHF12->SetBinContent(3,19.78015);
   VVHF12->SetBinContent(4,20.66903);
   VVHF12->SetBinContent(5,9.197353);
   VVHF12->SetBinContent(6,7.524415);
   VVHF12->SetBinContent(7,6.978524);
   VVHF12->SetBinContent(8,5.649176);
   VVHF12->SetBinContent(9,2.993247);
   VVHF12->SetBinContent(10,1.223999);
   VVHF12->SetBinContent(11,0.1241146);
   VVHF12->SetBinError(1,1.343859);
   VVHF12->SetBinError(2,1.377741);
   VVHF12->SetBinError(3,1.366464);
   VVHF12->SetBinError(4,1.318976);
   VVHF12->SetBinError(5,0.8945878);
   VVHF12->SetBinError(6,0.825684);
   VVHF12->SetBinError(7,0.8006608);
   VVHF12->SetBinError(8,0.6967201);
   VVHF12->SetBinError(9,0.5036871);
   VVHF12->SetBinError(10,0.3333731);
   VVHF12->SetBinError(11,0.08264953);
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
   1395.917,
   1092.4,
   770.3024,
   426.4051,
   134.117,
   99.18462,
   70.11752,
   34.97072,
   14.20715,
   3.986522,
   0.3513288};
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
   22.98773,
   20.34413,
   16.85754,
   12.35924,
   6.740752,
   5.9134,
   4.829652,
   2.219241,
   1.237308,
   0.5109903,
   0.1010653};
   TGraphErrors *gre = new TGraphErrors(11,Graph_from_VVHF_fx1001,Graph_from_VVHF_fy1001,Graph_from_VVHF_fex1001,Graph_from_VVHF_fey1001);
   gre->SetName("Graph_from_VVHF");
   gre->SetTitle("VVHF");

   ci = TColor::GetColor("#333333");
   gre->SetFillColor(ci);
   gre->SetFillStyle(3013);
   
   TH1F *Graph_Graph_from_VVHF1001 = new TH1F("Graph_Graph_from_VVHF1001","VVHF",100,0.12,1.08);
   Graph_Graph_from_VVHF1001->SetMinimum(0.2252372);
   Graph_Graph_from_VVHF1001->SetMaximum(1560.77);
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
   noData13->SetBinContent(0,18482);
   noData13->SetBinContent(1,1408);
   noData13->SetBinContent(2,1090);
   noData13->SetBinContent(3,753);
   noData13->SetBinContent(4,433);
   noData13->SetBinContent(5,127);
   noData13->SetBinContent(6,111);
   noData13->SetBinContent(7,70);
   noData13->SetBinContent(8,35);
   noData13->SetBinContent(9,13);
   noData13->SetBinContent(10,3);
   noData13->SetEntries(22525);
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
      tex = new TLatex(0.17,0.78,"1-lep (e)");
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
   Ratio14->SetBinContent(1,1.008656);
   Ratio14->SetBinContent(2,0.9978031);
   Ratio14->SetBinContent(3,0.9775381);
   Ratio14->SetBinContent(4,1.015466);
   Ratio14->SetBinContent(5,0.9469343);
   Ratio14->SetBinContent(6,1.119125);
   Ratio14->SetBinContent(7,0.9983239);
   Ratio14->SetBinContent(8,1.000837);
   Ratio14->SetBinContent(9,0.9150324);
   Ratio14->SetBinContent(10,0.7525357);
   Ratio14->SetBinContent(11,0.0001);
   Ratio14->SetBinError(1,0.02688077);
   Ratio14->SetBinError(2,0.03022258);
   Ratio14->SetBinError(3,0.03562347);
   Ratio14->SetBinError(4,0.0488002);
   Ratio14->SetBinError(5,0.08402683);
   Ratio14->SetBinError(6,0.1062227);
   Ratio14->SetBinError(7,0.1193225);
   Ratio14->SetBinError(8,0.1691724);
   Ratio14->SetBinError(9,0.2537843);
   Ratio14->SetBinError(10,0.4344767);
   Ratio14->SetBinError(11,5.123405);
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
   0.04022837,
   0.04265654,
   0.04987392,
   0.06523953,
   0.1060308,
   0.1360891,
   0.1378157,
   0.1361813,
   0.1837556,
   0.2442856,
   0.5568714};
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
   0.04022837,
   0.04265654,
   0.04987392,
   0.06523953,
   0.1060308,
   0.1360891,
   0.1378157,
   0.1361813,
   0.1837556,
   0.2442856,
   0.5568714};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(11,Graph_from_WH_hbb_postfit_fx3001,Graph_from_WH_hbb_postfit_fy3001,Graph_from_WH_hbb_postfit_felx3001,Graph_from_WH_hbb_postfit_fehx3001,Graph_from_WH_hbb_postfit_fely3001,Graph_from_WH_hbb_postfit_fehy3001);
   grae->SetName("Graph_from_WH_hbb_postfit");
   grae->SetTitle("WH_hbb_postfit");
   grae->SetFillColor(5);
   grae->SetFillStyle(3001);
   
   TH1F *Graph_Graph_from_WH_hbb_postfit3001 = new TH1F("Graph_Graph_from_WH_hbb_postfit3001","WH_hbb_postfit",100,0.12,1.08);
   Graph_Graph_from_WH_hbb_postfit3001->SetMinimum(0.3317544);
   Graph_Graph_from_WH_hbb_postfit3001->SetMaximum(1.668246);
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
   0.01646783,
   0.01862334,
   0.02188431,
   0.02898474,
   0.05026023,
   0.05962014,
   0.06887939,
   0.06345997,
   0.0870905,
   0.1281795,
   0.2876659};
   gre = new TGraphErrors(11,Graph_from_RefError_fx1002,Graph_from_RefError_fy1002,Graph_from_RefError_fex1002,Graph_from_RefError_fey1002);
   gre->SetName("Graph_from_RefError");
   gre->SetTitle("noData");

   ci = TColor::GetColor("#333333");
   gre->SetFillColor(ci);
   gre->SetFillStyle(3013);
   gre->SetLineStyle(0);
   gre->SetMarkerStyle(20);
   
   TH1F *Graph_Graph_from_RefError1002 = new TH1F("Graph_Graph_from_RefError1002","noData",100,0.12,1.08);
   Graph_Graph_from_RefError1002->SetMinimum(0.654801);
   Graph_Graph_from_RefError1002->SetMaximum(1.345199);
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
   Ratio15->SetBinContent(1,1.008656);
   Ratio15->SetBinContent(2,0.9978031);
   Ratio15->SetBinContent(3,0.9775381);
   Ratio15->SetBinContent(4,1.015466);
   Ratio15->SetBinContent(5,0.9469343);
   Ratio15->SetBinContent(6,1.119125);
   Ratio15->SetBinContent(7,0.9983239);
   Ratio15->SetBinContent(8,1.000837);
   Ratio15->SetBinContent(9,0.9150324);
   Ratio15->SetBinContent(10,0.7525357);
   Ratio15->SetBinContent(11,0.0001);
   Ratio15->SetBinError(1,0.02688077);
   Ratio15->SetBinError(2,0.03022258);
   Ratio15->SetBinError(3,0.03562347);
   Ratio15->SetBinError(4,0.0488002);
   Ratio15->SetBinError(5,0.08402683);
   Ratio15->SetBinError(6,0.1062227);
   Ratio15->SetBinError(7,0.1193225);
   Ratio15->SetBinError(8,0.1691724);
   Ratio15->SetBinError(9,0.2537843);
   Ratio15->SetBinError(10,0.4344767);
   Ratio15->SetBinError(11,5.123405);
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
