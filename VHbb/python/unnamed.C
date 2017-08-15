// Mainframe macro generated from application: /afs/cern.ch/cms/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd5/bin/root.exe
// By ROOT version 6.02/05 on 2017-07-19 22:29:05

#ifndef ROOT_TGFrame
#include "TGFrame.h"
#endif
#ifndef ROOT_TGMenu
#include "TGMenu.h"
#endif
#ifndef ROOT_TGListBox
#include "TGListBox.h"
#endif
#ifndef ROOT_TGScrollBar
#include "TGScrollBar.h"
#endif
#ifndef ROOT_TGComboBox
#include "TGComboBox.h"
#endif
#ifndef ROOT_TRootBrowser
#include "TRootBrowser.h"
#endif
#ifndef ROOT_TGFileDialog
#include "TGFileDialog.h"
#endif
#ifndef ROOT_TGButtonGroup
#include "TGButtonGroup.h"
#endif
#ifndef ROOT_TGCommandPlugin
#include "TGCommandPlugin.h"
#endif
#ifndef ROOT_TGCanvas
#include "TGCanvas.h"
#endif
#ifndef ROOT_TGFSContainer
#include "TGFSContainer.h"
#endif
#ifndef ROOT_TGButton
#include "TGButton.h"
#endif
#ifndef ROOT_TGTextEdit
#include "TGTextEdit.h"
#endif
#ifndef ROOT_TGFSComboBox
#include "TGFSComboBox.h"
#endif
#ifndef ROOT_TGLabel
#include "TGLabel.h"
#endif
#ifndef ROOT_TGView
#include "TGView.h"
#endif
#ifndef ROOT_TGFileBrowser
#include "TGFileBrowser.h"
#endif
#ifndef ROOT_TGTab
#include "TGTab.h"
#endif
#ifndef ROOT_TGListView
#include "TGListView.h"
#endif
#ifndef ROOT_TGSplitter
#include "TGSplitter.h"
#endif
#ifndef ROOT_TGTextEditor
#include "TGTextEditor.h"
#endif
#ifndef ROOT_TGTextEntry
#include "TGTextEntry.h"
#endif
#ifndef ROOT_TRootCanvas
#include "TRootCanvas.h"
#endif
#ifndef ROOT_TGDockableFrame
#include "TGDockableFrame.h"
#endif
#ifndef ROOT_TG3DLine
#include "TG3DLine.h"
#endif
#ifndef ROOT_TGStatusBar
#include "TGStatusBar.h"
#endif
#ifndef ROOT_TGListTree
#include "TGListTree.h"
#endif
#ifndef ROOT_TGToolTip
#include "TGToolTip.h"
#endif
#ifndef ROOT_TGToolBar
#include "TGToolBar.h"
#endif
#ifndef ROOT_TGHtmlBrowser
#include "TGHtmlBrowser.h"
#endif

#include "Riostream.h"

void unnamed()
{

   // main frame
   TGMainFrame *fRootBrowser2 = new TGMainFrame(gClient->GetRoot(),10,10,kMainFrame | kVerticalFrame);

   // vertical frame
   TGVerticalFrame *fVerticalFrame3 = new TGVerticalFrame(fRootBrowser2,800,482,kVerticalFrame);

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame4 = new TGHorizontalFrame(fVerticalFrame3,800,26,kHorizontalFrame);

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame5 = new TGHorizontalFrame(fHorizontalFrame4,59,26,kHorizontalFrame | kRaisedFrame);

   // menu bar
   TGMenuBar *fMenuBar6 = new TGMenuBar(fHorizontalFrame5,57,22,kHorizontalFrame);

   // "Browser" menu
   TGPopupMenu *fPopupMenu8 = new TGPopupMenu(gClient->GetDefaultRoot(),168,228,kOwnBackground);
   fPopupMenu8->AddEntry("&Browse...\tCtrl+B",11011);
   fPopupMenu8->AddEntry("&Open...\tCtrl+O",11012);
   fPopupMenu8->AddSeparator();

   // cascaded menu "Browser Help..."
   TGPopupMenu *fPopupMenu9 = new TGPopupMenu(gClient->GetDefaultRoot(),190,154,kOwnBackground);
   fPopupMenu9->AddEntry("&About ROOT...",11014);
   fPopupMenu9->AddSeparator();
   fPopupMenu9->AddEntry("Help On Browser...",11015);
   fPopupMenu9->AddEntry("Help On Canvas...",11016);
   fPopupMenu9->AddEntry("Help On Menus...",11017);
   fPopupMenu9->AddEntry("Help On Graphics Editor...",11018);
   fPopupMenu9->AddEntry("Help On Objects...",11019);
   fPopupMenu9->AddEntry("Help On PostScript...",11020);
   fPopupMenu9->AddEntry("Help On Remote Session...",11021);
   fPopupMenu8->AddPopup("Browser Help...",fPopupMenu9);
   fPopupMenu8->AddSeparator();
   fPopupMenu8->AddEntry("&Clone\tCtrl+N",11013);
   fPopupMenu8->AddSeparator();
   fPopupMenu8->AddEntry("New &Editor\tCtrl+E",11022);
   fPopupMenu8->AddEntry("New &Canvas\tCtrl+C",11023);
   fPopupMenu8->AddEntry("New &HTML\tCtrl+H",11024);
   fPopupMenu8->AddSeparator();

   // cascaded menu "Execute Plugin..."
   TGPopupMenu *fPopupMenu10 = new TGPopupMenu(gClient->GetDefaultRoot(),100,42,kOwnBackground);
   fPopupMenu10->AddEntry("&Macro...",11025);
   fPopupMenu10->AddEntry("&Command...",11026);
   fPopupMenu8->AddPopup("Execute &Plugin...",fPopupMenu10);
   fPopupMenu8->AddSeparator();
   fPopupMenu8->AddEntry("Close &Tab\tCtrl+T",11027);
   fPopupMenu8->AddEntry("Close &Window\tCtrl+W",11028);
   fPopupMenu8->AddSeparator();
   fPopupMenu8->AddEntry("&Quit Root\tCtrl+Q",11029);
   fMenuBar6->AddPopup("&Browser",fPopupMenu8, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));
   fHorizontalFrame5->AddFrame(fMenuBar6, new TGLayoutHints(kLHintsTop | kLHintsExpandX,0,0,1,1));

   fHorizontalFrame4->AddFrame(fHorizontalFrame5, new TGLayoutHints(kLHintsNormal));

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame12 = new TGHorizontalFrame(fHorizontalFrame4,741,26,kHorizontalFrame | kRaisedFrame);

   // menu bar
   TGMenuBar *fMenuBar115 = new TGMenuBar(fHorizontalFrame12,739,22,kHorizontalFrame);

   // "File" menu
   TGPopupMenu *fPopupMenu107 = new TGPopupMenu(gClient->GetDefaultRoot(),105,108,kOwnBackground);
   fPopupMenu107->AddEntry("&New Canvas",0);
   fPopupMenu107->AddEntry("&Open...",1);
   fPopupMenu107->AddEntry("&Close Canvas",12);
   fPopupMenu107->DisableEntry(12);
   fPopupMenu107->HideEntry(12);
   fPopupMenu107->AddSeparator();

   // cascaded menu "Save"
   TGPopupMenu *fPopupMenu106 = new TGPopupMenu(gClient->GetDefaultRoot(),116,150,kOwnBackground);
   fPopupMenu106->AddEntry("Canvas_1.&ps",5);
   fPopupMenu106->AddEntry("Canvas_1.&eps",6);
   fPopupMenu106->AddEntry("Canvas_1.p&df",7);
   fPopupMenu106->AddEntry("Canvas_1.&gif",8);
   fPopupMenu106->AddEntry("Canvas_1.&jpg",9);
   fPopupMenu106->AddEntry("Canvas_1.&png",10);
   fPopupMenu106->AddEntry("Canvas_1.&C",4);
   fPopupMenu106->AddEntry("Canvas_1.&root",3);
   fPopupMenu107->AddPopup("&Save",fPopupMenu106);
   fPopupMenu107->AddEntry("Save &As...",2);
   fPopupMenu107->AddSeparator();
   fPopupMenu107->AddEntry("&Print...",11);
   fPopupMenu107->AddSeparator();
   fPopupMenu107->AddEntry("&Quit ROOT",13);
   fPopupMenu107->DisableEntry(13);
   fPopupMenu107->HideEntry(13);
   fMenuBar115->AddPopup("&File",fPopupMenu107, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Edit" menu
   TGPopupMenu *fPopupMenu109 = new TGPopupMenu(gClient->GetDefaultRoot(),74,144,kOwnBackground);
   fPopupMenu109->AddEntry("&Style...",14);
   fPopupMenu109->AddSeparator();
   fPopupMenu109->AddEntry("Cu&t",15);
   fPopupMenu109->DisableEntry(15);
   fPopupMenu109->AddEntry("&Copy",16);
   fPopupMenu109->DisableEntry(16);
   fPopupMenu109->AddEntry("&Paste",17);
   fPopupMenu109->DisableEntry(17);
   fPopupMenu109->AddSeparator();

   // cascaded menu "Clear"
   TGPopupMenu *fPopupMenu108 = new TGPopupMenu(gClient->GetDefaultRoot(),74,42,kOwnBackground);
   fPopupMenu108->AddEntry("&Pad",18);
   fPopupMenu108->AddEntry("&Canvas",19);
   fPopupMenu109->AddPopup("C&lear",fPopupMenu108);
   fPopupMenu109->AddSeparator();
   fPopupMenu109->AddEntry("&Undo",20);
   fPopupMenu109->DisableEntry(20);
   fPopupMenu109->AddEntry("&Redo",21);
   fPopupMenu109->DisableEntry(21);
   fMenuBar115->AddPopup("&Edit",fPopupMenu109, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "View" menu
   TGPopupMenu *fPopupMenu111 = new TGPopupMenu(gClient->GetDefaultRoot(),128,180,kOwnBackground);
   fPopupMenu111->AddEntry("&Editor",22);
   fPopupMenu111->AddEntry("&Toolbar",23);
   fPopupMenu111->AddEntry("Event &Statusbar",24);
   fPopupMenu111->AddEntry("T&oolTip Info",25);
   fPopupMenu111->AddSeparator();
   fPopupMenu111->AddEntry("&Colors",26);
   fPopupMenu111->AddEntry("&Fonts",27);
   fPopupMenu111->DisableEntry(27);
   fPopupMenu111->AddEntry("&Markers",28);
   fPopupMenu111->AddSeparator();
   fPopupMenu111->AddEntry("&Iconify",29);
   fPopupMenu111->AddSeparator();

   // cascaded menu "View With"
   TGPopupMenu *fPopupMenu110 = new TGPopupMenu(gClient->GetDefaultRoot(),78,42,kOwnBackground);
   fPopupMenu110->AddEntry("&X3D",30);
   fPopupMenu110->AddEntry("&OpenGL",31);
   fPopupMenu111->AddPopup("&View With",fPopupMenu110);
   fMenuBar115->AddPopup("&View",fPopupMenu111, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Options" menu
   TGPopupMenu *fPopupMenu112 = new TGPopupMenu(gClient->GetDefaultRoot(),151,216,kOwnBackground);
   fPopupMenu112->AddEntry("&Auto Resize Canvas",32);
   fPopupMenu112->CheckEntry(32);
   fPopupMenu112->AddEntry("&Resize Canvas",33);
   fPopupMenu112->AddEntry("&Move Opaque",34);
   fPopupMenu112->CheckEntry(34);
   fPopupMenu112->AddEntry("Resize &Opaque",35);
   fPopupMenu112->CheckEntry(35);
   fPopupMenu112->AddSeparator();
   fPopupMenu112->AddEntry("&Interrupt",36);
   fPopupMenu112->AddEntry("R&efresh",37);
   fPopupMenu112->AddSeparator();
   fPopupMenu112->AddEntry("&Pad Auto Exec",38);
   fPopupMenu112->AddSeparator();
   fPopupMenu112->AddEntry("&Statistics",39);
   fPopupMenu112->CheckEntry(39);
   fPopupMenu112->AddEntry("Histogram &Title",40);
   fPopupMenu112->CheckEntry(40);
   fPopupMenu112->AddEntry("&Fit Parameters",41);
   fPopupMenu112->AddEntry("Can Edit &Histograms",42);
   fMenuBar115->AddPopup("&Options",fPopupMenu112, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Tools" menu
   TGPopupMenu *fPopupMenu113 = new TGPopupMenu(gClient->GetDefaultRoot(),123,114,kOwnBackground);
   fPopupMenu113->AddEntry("&Inspect ROOT",43);
   fPopupMenu113->AddEntry("&Class Tree",44);
   fPopupMenu113->AddEntry("&Fit Panel",45);
   fPopupMenu113->AddEntry("&Start Browser",46);
   fPopupMenu113->AddEntry("&Gui Builder",47);
   fPopupMenu113->AddEntry("&Event Recorder",48);
   fMenuBar115->AddPopup("&Tools",fPopupMenu113, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Help" menu
   TGPopupMenu *fPopupMenu114 = new TGPopupMenu(gClient->GetDefaultRoot(),126,158,kOwnBackground);
   fPopupMenu114->AddLabel("Basic Help On...");
   fPopupMenu114->DefaultEntry(-1);
   fPopupMenu114->AddSeparator();
   fPopupMenu114->AddEntry("&Canvas",50);
   fPopupMenu114->AddEntry("&Menus",51);
   fPopupMenu114->AddEntry("&Graphics Editor",52);
   fPopupMenu114->AddEntry("&Browser",53);
   fPopupMenu114->AddEntry("&Objects",54);
   fPopupMenu114->AddEntry("&PostScript",55);
   fPopupMenu114->AddSeparator();
   fPopupMenu114->AddEntry("&About ROOT...",49);
   fMenuBar115->AddPopup("&Help",fPopupMenu114, new TGLayoutHints(kLHintsRight | kLHintsTop));
   fHorizontalFrame12->AddFrame(fMenuBar115, new TGLayoutHints(kLHintsTop | kLHintsExpandX,0,0,1,1));

   // menu bar
   TGMenuBar *fMenuBar160 = new TGMenuBar(fHorizontalFrame12,739,22,kHorizontalFrame);

   // "File" menu
   TGPopupMenu *fPopupMenu155 = new TGPopupMenu(gClient->GetDefaultRoot(),92,126,kOwnBackground);
   fPopupMenu155->AddEntry("&New",0);
   fPopupMenu155->AddSeparator();
   fPopupMenu155->AddEntry("&Open...",1);
   fPopupMenu155->AddEntry("&Close",4);
   fPopupMenu155->AddEntry("&Save",2);
   fPopupMenu155->AddEntry("Save &As...",3);
   fPopupMenu155->AddSeparator();
   fPopupMenu155->AddEntry("&Print...",5);
   fPopupMenu155->AddSeparator();
   fPopupMenu155->AddEntry("E&xit",6);
   fPopupMenu155->DisableEntry(6);
   fPopupMenu155->HideEntry(6);
   fMenuBar160->AddPopup("&File",fPopupMenu155, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Edit" menu
   TGPopupMenu *fPopupMenu156 = new TGPopupMenu(gClient->GetDefaultRoot(),141,122,kOwnBackground);
   fPopupMenu156->AddEntry("Cu&t\tCtrl+X",7);
   fPopupMenu156->DisableEntry(7);
   fPopupMenu156->AddEntry("&Copy\tCtrl+C",8);
   fPopupMenu156->DisableEntry(8);
   fPopupMenu156->AddEntry("&Paste\tCtrl+V",9);
   fPopupMenu156->AddEntry("De&lete\tDel",10);
   fPopupMenu156->DisableEntry(10);
   fPopupMenu156->AddSeparator();
   fPopupMenu156->AddEntry("Select &All\tCtrl+A",11);
   fPopupMenu156->AddSeparator();
   fPopupMenu156->AddEntry("Set &Font",20);
   fMenuBar160->AddPopup("&Edit",fPopupMenu156, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Search" menu
   TGPopupMenu *fPopupMenu158 = new TGPopupMenu(gClient->GetDefaultRoot(),153,64,kOwnBackground);
   fPopupMenu158->AddEntry("&Find...\tCtrl+F",12);
   fPopupMenu158->AddEntry("Find &Next\tF3",13);
   fPopupMenu158->AddSeparator();
   fPopupMenu158->AddEntry("&Goto Line...\tCtrl+L",14);
   fMenuBar160->AddPopup("&Search",fPopupMenu158, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Tools" menu
   TGPopupMenu *fPopupMenu157 = new TGPopupMenu(gClient->GetDefaultRoot(),180,60,kOwnBackground);
   fPopupMenu157->AddEntry("&Compile Macro\tCtrl+F7",15);
   fPopupMenu157->AddEntry("&Execute Macro\tCtrl+F5",16);
   fPopupMenu157->AddEntry("&Interrupt\tShift+F5",17);
   fMenuBar160->AddPopup("&Tools",fPopupMenu157, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Help" menu
   TGPopupMenu *fPopupMenu159 = new TGPopupMenu(gClient->GetDefaultRoot(),132,46,kOwnBackground);
   fPopupMenu159->AddEntry("&Help Topics\tF1",18);
   fPopupMenu159->AddSeparator();
   fPopupMenu159->AddEntry("&About...",19);
   fMenuBar160->AddPopup("&Help",fPopupMenu159, new TGLayoutHints(kLHintsRight | kLHintsTop));
   fHorizontalFrame12->AddFrame(fMenuBar160, new TGLayoutHints(kLHintsTop | kLHintsExpandX,0,0,1,1));

   fHorizontalFrame4->AddFrame(fHorizontalFrame12, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));

   fVerticalFrame3->AddFrame(fHorizontalFrame4, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX));

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame13 = new TGHorizontalFrame(fVerticalFrame3,400,2,kHorizontalFrame | kRaisedFrame);

   fVerticalFrame3->AddFrame(fHorizontalFrame13, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX));

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame14 = new TGHorizontalFrame(fVerticalFrame3,800,456,kHorizontalFrame);

   // vertical frame
   TGVerticalFrame *fVerticalFrame15 = new TGVerticalFrame(fHorizontalFrame14,250,456,kVerticalFrame | kFixedWidth);

   // tab widget
   TGTab *fTab19 = new TGTab(fVerticalFrame15,246,452);

   // container of "Files"
   TGCompositeFrame *fCompositeFrame34;
   fCompositeFrame34 = fTab19->AddTab("Files");
   fCompositeFrame34->SetLayoutManager(new TGVerticalLayout(fCompositeFrame34));

   // composite frame
   TGCompositeFrame *fFileBrowser35 = new TGCompositeFrame(fCompositeFrame34,242,427,kVerticalFrame);

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame36 = new TGHorizontalFrame(fFileBrowser35,238,26,kHorizontalFrame);

   ULong_t ucolor;        // will reflect user color changes
   gClient->GetColorByName("#ffffff",ucolor);

   // combo box
   TGComboBox *fComboBox37 = new TGComboBox(fHorizontalFrame36,"",-1,kHorizontalFrame | kSunkenFrame | kDoubleBorder | kOwnBackground);
   fComboBox37->AddEntry("",1);
   fComboBox37->AddEntry("box",2);
   fComboBox37->AddEntry("colz",3);
   fComboBox37->AddEntry("lego",4);
   fComboBox37->AddEntry("lego1",5);
   fComboBox37->AddEntry("lego2",6);
   fComboBox37->AddEntry("same",7);
   fComboBox37->AddEntry("surf",8);
   fComboBox37->AddEntry("surf1",9);
   fComboBox37->AddEntry("surf2",10);
   fComboBox37->AddEntry("surf3",11);
   fComboBox37->AddEntry("surf4",12);
   fComboBox37->AddEntry("surf5",13);
   fComboBox37->AddEntry("text",14);
   fComboBox37->Resize(80,20);
   fComboBox37->Select(-1);
   fHorizontalFrame36->AddFrame(fComboBox37, new TGLayoutHints(kLHintsRight | kLHintsCenterY,2,2,2,2));
   TGLabel *fLabel64 = new TGLabel(fHorizontalFrame36,"Draw Option:");
   fLabel64->SetTextJustify(36);
   fLabel64->SetMargins(0,0,0,0);
   fLabel64->SetWrapLength(-1);
   fHorizontalFrame36->AddFrame(fLabel64, new TGLayoutHints(kLHintsRight | kLHintsCenterY,5,2,2,2));
   TGPictureButton *fPictureButton65 = new TGPictureButton(fHorizontalFrame36,gClient->GetPicture("bld_sortup.png"),-1,TGPictureButton::GetDefaultGC()(),kDoubleBorder);
   fPictureButton65->SetToolTipText("Sort Alphabetically\n(Current folder only)");
   fHorizontalFrame36->AddFrame(fPictureButton65, new TGLayoutHints(kLHintsLeft | kLHintsCenterY,2,2,2,2));
   fPictureButton65->Connect("Clicked()", 0, 0, "ToggleSort()");
   TGPictureButton *fPictureButton68 = new TGPictureButton(fHorizontalFrame36,gClient->GetPicture("filter.png"),-1,TGPictureButton::GetDefaultGC()(),kDoubleBorder);
   fPictureButton68->SetToolTipText("Filter Content");
   fHorizontalFrame36->AddFrame(fPictureButton68, new TGLayoutHints(kLHintsLeft | kLHintsCenterY,2,2,2,2));
   fPictureButton68->Connect("Clicked()", 0, 0, "RequestFilter()");
   TGPictureButton *fPictureButton71 = new TGPictureButton(fHorizontalFrame36,gClient->GetPicture("refresh.png"),-1,TGPictureButton::GetDefaultGC()(),kDoubleBorder);
   fPictureButton71->SetToolTipText("Refresh Current Folder");
   fHorizontalFrame36->AddFrame(fPictureButton71, new TGLayoutHints(kLHintsLeft | kLHintsCenterY,2,5,2,2));
   fPictureButton71->Connect("Clicked()", 0, 0, "Refresh()");

   fFileBrowser35->AddFrame(fHorizontalFrame36, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX,2,2,2,2));

   // canvas widget
   TGCanvas *fCanvas74 = new TGCanvas(fFileBrowser35,242,369);

   // canvas viewport
   TGViewPort *fViewPort75 = fCanvas74->GetViewPort();

   // list tree
   TGListTree *fListTree84 = new TGListTree(fCanvas74,kHorizontalFrame);

   const TGPicture *popen;       //used for list tree items
   const TGPicture *pclose;      //used for list tree items

   TGListTreeItem *item0 = fListTree84->AddItem(NULL,"root");
   popen = gClient->GetPicture("ofolder_t.xpm");
   pclose = gClient->GetPicture("folder_t.xpm");
   item0->SetPictures(popen, pclose);
   item0->SetTipText("root\nroot of all folders");
   fListTree84->CloseItem(item0);
   TGListTreeItem *item1 = fListTree84->AddItem(NULL,"PROOF Sessions");
   item1->SetPictures(popen, pclose);
   item1->SetTipText("Proofs\nDoubly linked list");
   fListTree84->CloseItem(item1);
   TGListTreeItem *item2 = fListTree84->AddItem(NULL,"ROOT Files");
   item2->SetPictures(popen, pclose);
   item2->SetTipText("Files\nDoubly linked list");
   fListTree84->OpenItem(item2);
   TGListTreeItem *item3 = fListTree84->AddItem(item2,"/exports/uftrig01a/dcurry/heppy/files/MVA_out_VV/v25_ZH125.root");
   popen = gClient->GetPicture("rootdb_t.xpm__16x16");
   pclose = gClient->GetPicture("rootdb_t.xpm__16x16");
   item3->SetPictures(popen, pclose);
   item3->SetTipText("/exports/uftrig01a/dcurry/hep...");
   TGListTreeItem *item4 = fListTree84->AddItem(NULL,"/");
   popen = gClient->GetPicture("ofolder_t.xpm");
   pclose = gClient->GetPicture("folder_t.xpm");
   item4->SetPictures(popen, pclose);
   fListTree84->OpenItem(item4);
   TGListTreeItem *item5 = fListTree84->AddItem(item4,"afs");
   item5->SetPictures(popen, pclose);
   TGListTreeItem *item6 = fListTree84->AddItem(item5,"cern.ch");
   item6->SetPictures(popen, pclose);
   TGListTreeItem *item7 = fListTree84->AddItem(item6,"work");
   item7->SetPictures(popen, pclose);
   TGListTreeItem *item8 = fListTree84->AddItem(item7,"d");
   item8->SetPictures(popen, pclose);
   TGListTreeItem *item9 = fListTree84->AddItem(item8,"dcurry");
   item9->SetPictures(popen, pclose);
   TGListTreeItem *item10 = fListTree84->AddItem(item9,"public");
   item10->SetPictures(popen, pclose);
   TGListTreeItem *item11 = fListTree84->AddItem(item10,"v25Heppy");
   item11->SetPictures(popen, pclose);
   TGListTreeItem *item12 = fListTree84->AddItem(item11,"CMSSW_7_4_7");
   item12->SetPictures(popen, pclose);
   TGListTreeItem *item13 = fListTree84->AddItem(item12,"src");
   item13->SetPictures(popen, pclose);
   TGListTreeItem *item14 = fListTree84->AddItem(item13,"VHbb");
   item14->SetPictures(popen, pclose);
   TGListTreeItem *item15 = fListTree84->AddItem(item14,"python");
   item15->SetPictures(popen, pclose);
   TGListTreeItem *item16 = fListTree84->AddItem(item15,"13TeVconfig");
   item16->SetPictures(popen, pclose);
   TGListTreeItem *item17 = fListTree84->AddItem(item15,"heppy13TeVconfig");
   item17->SetPictures(popen, pclose);
   TGListTreeItem *item18 = fListTree84->AddItem(item15,"myutils");
   item18->SetPictures(popen, pclose);
   TGListTreeItem *item19 = fListTree84->AddItem(item15,"results");
   item19->SetPictures(popen, pclose);
   TGListTreeItem *item20 = fListTree84->AddItem(item15,"v25_CR_CMVA_LO_4_9");
   item20->SetPictures(popen, pclose);
   TGListTreeItem *item21 = fListTree84->AddItem(item15,"weights");
   item21->SetPictures(popen, pclose);
   TGListTreeItem *item22 = fListTree84->AddItem(item15,"#plot_systematics.py#");
   popen = gClient->GetPicture("doc_t.xpm");
   pclose = gClient->GetPicture("doc_t.xpm");
   item22->SetPictures(popen, pclose);
   item22->SetTipText("#plot_systematics.py#\nSize: 11.1K\n2017-07-04 09:50");
   TGListTreeItem *item23 = fListTree84->AddItem(item15,"BTagCalibrationStandalone.o");
   item23->SetPictures(popen, pclose);
   item23->SetTipText("BTagCalibrationStandalone.o\nSize: 96.9K\n2017-01-30 16:02");
   TGListTreeItem *item24 = fListTree84->AddItem(item15,"BTagCalibrationStandalone.so");
   item24->SetPictures(popen, pclose);
   item24->SetTipText("BTagCalibrationStandalone.so\nSize: 413.8K\n2017-01-30 16:02");
   TGListTreeItem *item25 = fListTree84->AddItem(item15,"CSVv2_Moriond17_B_H.csv");
   item25->SetPictures(popen, pclose);
   item25->SetTipText("CSVv2_Moriond17_B_H.csv\nSize: 171.1K\n2017-03-17 21:58");
   TGListTreeItem *item26 = fListTree84->AddItem(item15,"FactorizedSYS_writeRegZll.py");
   item26->SetPictures(popen, pclose);
   item26->SetTipText("FactorizedSYS_writeRegZll.py\nSize: 41.5K\n2017-05-15 18:30");
   TGListTreeItem *item27 = fListTree84->AddItem(item15,"Jet_sys_decorrelation.py");
   item27->SetPictures(popen, pclose);
   item27->SetTipText("Jet_sys_decorrelation.py\nSize: 8.8K\n2017-03-20 22:44");
   TGListTreeItem *item28 = fListTree84->AddItem(item15,"VtypeReEvaluation.py");
   item28->SetPictures(popen, pclose);
   item28->SetTipText("VtypeReEvaluation.py\nSize: 12.3K\n2017-05-15 18:20");
   TGListTreeItem *item29 = fListTree84->AddItem(item15,"addSOverBWeight.py");
   item29->SetPictures(popen, pclose);
   item29->SetTipText("addSOverBWeight.py\nSize: 8.5K\n2017-05-09 19:32");
   TGListTreeItem *item30 = fListTree84->AddItem(item15,"addingSamples.py");
   item30->SetPictures(popen, pclose);
   item30->SetTipText("addingSamples.py\nSize: 6.6K\n2017-01-30 16:02");
   TGListTreeItem *item31 = fListTree84->AddItem(item15,"bTagSF.py");
   item31->SetPictures(popen, pclose);
   item31->SetTipText("bTagSF.py\nSize: 18.0K\n2017-05-17 17:39");
   TGListTreeItem *item32 = fListTree84->AddItem(item15,"cMVAv2_Moriond17_B_H.csv");
   item32->SetPictures(popen, pclose);
   item32->SetTipText("cMVAv2_Moriond17_B_H.csv\nSize: 150.5K\n2017-03-17 21:59");
   TGListTreeItem *item33 = fListTree84->AddItem(item15,"check_for_duplicates.py");
   item33->SetPictures(popen, pclose);
   item33->SetTipText("check_for_duplicates.py\nSize: 1.7K\n2017-01-30 16:02");
   TGListTreeItem *item34 = fListTree84->AddItem(item15,"cls_expected.txt");
   item34->SetPictures(popen, pclose);
   TGListTreeItem *item35 = fListTree84->AddItem(item15,"config_unroller.py");
   item35->SetPictures(popen, pclose);
   item35->SetTipText("config_unroller.py\nSize: 768\n2017-01-30 16:02");
   TGListTreeItem *item36 = fListTree84->AddItem(item15,"controlPlot.py");
   item36->SetPictures(popen, pclose);
   item36->SetTipText("controlPlot.py\nSize: 3.4K\n2017-01-30 16:02");
   TGListTreeItem *item37 = fListTree84->AddItem(item15,"copyData_obs.py");
   item37->SetPictures(popen, pclose);
   item37->SetTipText("copyData_obs.py\nSize: 2.5K\n2017-01-30 16:02");
   TGListTreeItem *item38 = fListTree84->AddItem(item15,"dc_tex_converter.py");
   item38->SetPictures(popen, pclose);
   item38->SetTipText("dc_tex_converter.py\nSize: 1.7K\n2017-01-30 16:02");
   TGListTreeItem *item39 = fListTree84->AddItem(item15,"diffNuisances.py");
   item39->SetPictures(popen, pclose);
   item39->SetTipText("diffNuisances.py\nSize: 18.1K\n2017-01-30 16:02");
   TGListTreeItem *item40 = fListTree84->AddItem(item15,"evaluateMVA.py");
   item40->SetPictures(popen, pclose);
   item40->SetTipText("evaluateMVA.py\nSize: 5.0K\n2017-05-01 19:33");
   TGListTreeItem *item41 = fListTree84->AddItem(item15,"ggZH125_ext2_hadd.txt");
   item41->SetPictures(popen, pclose);
   item41->SetTipText("ggZH125_ext2_hadd.txt\nSize: 3.4K\n2017-04-10 20:57");
   TGListTreeItem *item42 = fListTree84->AddItem(item15,"gravall-v25.weights.xml");
   item42->SetPictures(popen, pclose);
   item42->SetTipText("gravall-v25.weights.xml\nSize: 20.5M\n2017-03-29 16:41");
   TGListTreeItem *item43 = fListTree84->AddItem(item15,"kinFit_Hmass.py");
   item43->SetPictures(popen, pclose);
   item43->SetTipText("kinFit_Hmass.py\nSize: 5.4K\n2017-01-30 16:02");
   TGListTreeItem *item44 = fListTree84->AddItem(item15,"lxplusbatchscript.csh");
   item44->SetPictures(popen, pclose);
   item44->SetTipText("lxplusbatchscript.csh\nSize: 350\n2017-03-17 15:08");
   TGListTreeItem *item45 = fListTree84->AddItem(item15,"manualStack.py");
   item45->SetPictures(popen, pclose);
   item45->SetTipText("manualStack.py\nSize: 20.2K\n2017-01-30 16:02");
   TGListTreeItem *item46 = fListTree84->AddItem(item15,"mlfit.root");
   popen = gClient->GetPicture("rootdb_t.xpm__16x16");
   pclose = gClient->GetPicture("rootdb_t.xpm__16x16");
   item46->SetPictures(popen, pclose);
   item46->SetTipText("mlfit.root\nSize: 7.8M\n2017-07-19 17:53");
   TGListTreeItem *item47 = fListTree84->AddItem(item15,"mvainfos.py");
   popen = gClient->GetPicture("doc_t.xpm");
   pclose = gClient->GetPicture("doc_t.xpm");
   item47->SetPictures(popen, pclose);
   item47->SetTipText("mvainfos.py\nSize: 903\n2017-01-30 16:02");
   TGListTreeItem *item48 = fListTree84->AddItem(item15,"plot_systematics.py");
   item48->SetPictures(popen, pclose);
   item48->SetTipText("plot_systematics.py\nSize: 10.9K\n2017-07-04 13:31");
   TGListTreeItem *item49 = fListTree84->AddItem(item15,"prepare_environment_with_config.py");
   item49->SetPictures(popen, pclose);
   item49->SetTipText("prepare_environment_with_config.py\nSize: 1.0K\n2017-01-30 16:02");
   TGListTreeItem *item50 = fListTree84->AddItem(item15,"producePlots.py");
   item50->SetPictures(popen, pclose);
   item50->SetTipText("producePlots.py\nSize: 2.9K\n2017-01-30 16:02");
   TGListTreeItem *item51 = fListTree84->AddItem(item15,"roc_depth_highPt.txt");
   item51->SetPictures(popen, pclose);
   item51->SetTipText("roc_depth_highPt.txt\nSize: 45\n2017-04-22 17:41");
   TGListTreeItem *item52 = fListTree84->AddItem(item15,"roc_depth_lowPt.txt");
   item52->SetPictures(popen, pclose);
   item52->SetTipText("roc_depth_lowPt.txt\nSize: 75\n2017-04-22 08:29");
   TGListTreeItem *item53 = fListTree84->AddItem(item15,"roc_lr_highPt.txt");
   item53->SetPictures(popen, pclose);
   item53->SetTipText("roc_lr_highPt.txt\nSize: 30\n2017-04-22 18:32");
   TGListTreeItem *item54 = fListTree84->AddItem(item15,"roc_lr_lowPt.txt");
   item54->SetPictures(popen, pclose);
   item54->SetTipText("roc_lr_lowPt.txt\nSize: 164\n2017-04-22 14:52");
   TGListTreeItem *item55 = fListTree84->AddItem(item15,"roc_nEvt_highPt.txt");
   item55->SetPictures(popen, pclose);
   item55->SetTipText("roc_nEvt_highPt.txt\nSize: 45\n2017-04-22 18:02");
   TGListTreeItem *item56 = fListTree84->AddItem(item15,"roc_nEvt_lowPt.txt");
   item56->SetPictures(popen, pclose);
   item56->SetTipText("roc_nEvt_lowPt.txt\nSize: 178\n2017-04-22 10:51");
   TGListTreeItem *item57 = fListTree84->AddItem(item15,"roc_node_cut_highPt.txt");
   item57->SetPictures(popen, pclose);
   item57->SetTipText("roc_node_cut_highPt.txt\nSize: 30\n2017-04-22 18:23");
   TGListTreeItem *item58 = fListTree84->AddItem(item15,"roc_node_cut_lowPt.txt");
   item58->SetPictures(popen, pclose);
   item58->SetTipText("roc_node_cut_lowPt.txt\nSize: 120\n2017-04-22 12:33");
   TGListTreeItem *item59 = fListTree84->AddItem(item15,"roc_temp.txt");
   item59->SetPictures(popen, pclose);
   item59->SetTipText("roc_temp.txt\nSize: 45\n2017-04-22 18:57");
   TGListTreeItem *item60 = fListTree84->AddItem(item15,"roc_trees_highPt.txt");
   item60->SetPictures(popen, pclose);
   item60->SetTipText("roc_trees_highPt.txt\nSize: 224\n2017-04-22 17:14");
   TGListTreeItem *item61 = fListTree84->AddItem(item15,"roc_trees_lowPt.txt");
   item61->SetPictures(popen, pclose);
   item61->SetTipText("roc_trees_lowPt.txt\nSize: 194\n2017-04-22 07:28");
   TGListTreeItem *item62 = fListTree84->AddItem(item15,"runAll.sh");
   item62->SetPictures(popen, pclose);
   item62->SetTipText("runAll.sh\nSize: 6.0K\n2017-01-30 16:02");
   TGListTreeItem *item63 = fListTree84->AddItem(item15,"scaleFactorPlot.py");
   item63->SetPictures(popen, pclose);
   item63->SetTipText("scaleFactorPlot.py\nSize: 28.4K\n2017-01-30 16:02");
   TGListTreeItem *item64 = fListTree84->AddItem(item15,"split_tree.py");
   item64->SetPictures(popen, pclose);
   item64->SetTipText("split_tree.py\nSize: 2.3K\n2017-01-30 16:02");
   TGListTreeItem *item65 = fListTree84->AddItem(item15,"stack_from_dc.py");
   item65->SetPictures(popen, pclose);
   item65->SetTipText("stack_from_dc.py\nSize: 28.8K\n2017-07-13 17:21");
   TGListTreeItem *item66 = fListTree84->AddItem(item15,"stack_from_dc_Mjj.py");
   item66->SetPictures(popen, pclose);
   item66->SetTipText("stack_from_dc_Mjj.py\nSize: 24.7K\n2017-07-12 15:23");
   TGListTreeItem *item67 = fListTree84->AddItem(item15,"stack_from_dc_Mjj.py~");
   item67->SetPictures(popen, pclose);
   item67->SetTipText("stack_from_dc_Mjj.py~\nSize: 24.8K\n2017-07-12 15:21");
   TGListTreeItem *item68 = fListTree84->AddItem(item15,"stack_from_dc_NEW.py");
   item68->SetPictures(popen, pclose);
   item68->SetTipText("stack_from_dc_NEW.py\nSize: 25.2K\n2017-07-13 19:14");
   TGListTreeItem *item69 = fListTree84->AddItem(item15,"submitThem.py");
   item69->SetPictures(popen, pclose);
   item69->SetTipText("submitThem.py\nSize: 10.9K\n2017-03-29 20:35");
   TGListTreeItem *item70 = fListTree84->AddItem(item15,"train.py");
   item70->SetPictures(popen, pclose);
   item70->SetTipText("train.py\nSize: 9.9K\n2017-04-22 18:36");
   TGListTreeItem *item71 = fListTree84->AddItem(item15,"trainRegression.py");
   item71->SetPictures(popen, pclose);
   item71->SetTipText("trainRegression.py\nSize: 648\n2017-01-30 16:02");
   TGListTreeItem *item72 = fListTree84->AddItem(item15,"tree_stack.py");
   item72->SetPictures(popen, pclose);
   item72->SetTipText("tree_stack.py\nSize: 5.7K\n2017-02-20 19:34");
   TGListTreeItem *item73 = fListTree84->AddItem(item15,"ttH_BTV_CSVv2_13TeV_2016All_36p5_2017_1_10.csv");
   item73->SetPictures(popen, pclose);
   item73->SetTipText("ttH_BTV_CSVv2_13TeV_2016All_36p5_2017_1_10.csv\nSize: 140.4K\n2017-02-10 20:52");
   TGListTreeItem *item74 = fListTree84->AddItem(item15,"ttH_BTV_cMVAv2_13TeV_2016All_36p5_2017_1_26.csv");
   item74->SetPictures(popen, pclose);
   item74->SetTipText("ttH_BTV_cMVAv2_13TeV_2016All_36p5_2017_1_26.csv\nSize: 136.5K\n2017-01-31 23:56");
   TGListTreeItem *item75 = fListTree84->AddItem(item15,"ttbar-G25-500k-13d-300t.weights.xml");
   item75->SetPictures(popen, pclose);
   item75->SetTipText("ttbar-G25-500k-13d-300t.weights.xml\nSize: 21.9M\n2017-02-24 23:56");
   TGListTreeItem *item76 = fListTree84->AddItem(item15,"workspace_datacard.py");
   item76->SetPictures(popen, pclose);
   item76->SetTipText("workspace_datacard.py\nSize: 46.2K\n2017-07-19 18:03");
   TGListTreeItem *item77 = fListTree84->AddItem(item15,"writeRegZll.py");
   item77->SetPictures(popen, pclose);
   item77->SetTipText("writeRegZll.py\nSize: 13.7K\n2017-01-30 16:02");
   TGListTreeItem *item78 = fListTree84->AddItem(item15,"write_regression_systematics.py");
   item78->SetPictures(popen, pclose);
   item78->SetTipText("write_regression_systematics.py\nSize: 53.2K\n2017-05-01 16:45");
   TGListTreeItem *item79 = fListTree84->AddItem(item15,"write_regression_systematics_ETH.py");
   item79->SetPictures(popen, pclose);
   item79->SetTipText("write_regression_systematics_ETH.py\nSize: 5.8K\n2017-01-30 16:02");

   fViewPort75->AddFrame(fListTree84);
   fListTree84->SetLayoutManager(new TGHorizontalLayout(fListTree84));
   fListTree84->MapSubwindows();
   fCanvas74->SetContainer(fListTree84);
   fCanvas74->MapSubwindows();
   fCanvas74->SetHsbPosition(0);
   fCanvas74->SetVsbPosition(0);
   fFileBrowser35->AddFrame(fCanvas74, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame85 = new TGHorizontalFrame(fFileBrowser35,238,24,kHorizontalFrame);
   TGLabel *fLabel86 = new TGLabel(fHorizontalFrame85,"Filter: ");
   fLabel86->SetTextJustify(36);
   fLabel86->SetMargins(0,0,0,0);
   fLabel86->SetWrapLength(-1);
   fHorizontalFrame85->AddFrame(fLabel86, new TGLayoutHints(kLHintsLeft | kLHintsCenterY,2,2,2,2));

   gClient->GetColorByName("#ffffff",ucolor);

   // combo box
   TGComboBox *fComboBox87 = new TGComboBox(fHorizontalFrame85," All Files (*.*)",-1,kHorizontalFrame | kSunkenFrame | kDoubleBorder | kOwnBackground);
   fComboBox87->AddEntry(" All Files (*.*)",1);
   fComboBox87->AddEntry(" C/C++ Files (*.c;*.cxx;*.h;...)",2);
   fComboBox87->AddEntry(" ROOT Files (*.root)",3);
   fComboBox87->AddEntry(" Text Files (*.txt)",4);
   fComboBox87->Resize(195,20);
   fComboBox87->Select(-1);
   fHorizontalFrame85->AddFrame(fComboBox87, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX,2,2,2,2));
   fComboBox87->Connect("Selected(int)", 0, 0, "ApplyFilter(int)");

   fFileBrowser35->AddFrame(fHorizontalFrame85, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX,2,2,2,2));

   fCompositeFrame34->AddFrame(fFileBrowser35, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
   fFileBrowser35->Connect("ProcessedConfigure(Event_t*)", 0, 0, "Layout()");


   fTab19->SetTab(0);

   fTab19->Resize(fTab19->GetDefaultSize());
   fVerticalFrame15->AddFrame(fTab19, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY,2,2,2,2));

   fHorizontalFrame14->AddFrame(fVerticalFrame15, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandY));
   TGVSplitter *fVSplitter21 = new TGVSplitter(fHorizontalFrame14,4,456);
   fVSplitter21->SetFrame(fVerticalFrame15,kTRUE);
   fHorizontalFrame14->AddFrame(fVSplitter21, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandY));

   // vertical frame
   TGVerticalFrame *fVerticalFrame16 = new TGVerticalFrame(fHorizontalFrame14,546,456,kVerticalFrame);

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame17 = new TGHorizontalFrame(fVerticalFrame16,542,348,kHorizontalFrame);

   // tab widget
   TGTab *fTab22 = new TGTab(fHorizontalFrame17,542,348);

   // container of "Canvas_1"
   TGCompositeFrame *fCompositeFrame104;
   fCompositeFrame104 = fTab22->AddTab("Canvas_1");
   fCompositeFrame104->SetLayoutManager(new TGVerticalLayout(fCompositeFrame104));

   // composite frame
   TGCompositeFrame *fRootCanvas105 = new TGCompositeFrame(fCompositeFrame104,538,323,kVerticalFrame);
   TGHorizontal3DLine *fHorizontal3DLine123 = new TGHorizontal3DLine(fRootCanvas105,700,2);
   fRootCanvas105->AddFrame(fHorizontal3DLine123, new TGLayoutHints(kLHintsTop | kLHintsExpandX));

   // dockable frame
   TGDockableFrame *fDockableFrame124 = new TGDockableFrame(fRootCanvas105);

   // next lines belong to the dockable frame widget
   fDockableFrame124->EnableUndock(kTRUE);
   fDockableFrame124->EnableHide(kFALSE);
   fDockableFrame124->SetWindowName("ToolBar: Canvas_1");
   fDockableFrame124->DockContainer();

   fRootCanvas105->AddFrame(fDockableFrame124, new TGLayoutHints(kLHintsExpandX));
   TGHorizontal3DLine *fHorizontal3DLine129 = new TGHorizontal3DLine(fRootCanvas105,700,2);
   fRootCanvas105->AddFrame(fHorizontal3DLine129, new TGLayoutHints(kLHintsTop | kLHintsExpandX));

   // composite frame
   TGCompositeFrame *fCompositeFrame130 = new TGCompositeFrame(fRootCanvas105,538,323,kHorizontalFrame);

   // composite frame
   TGCompositeFrame *fCompositeFrame131 = new TGCompositeFrame(fCompositeFrame130,175,476,kFixedWidth);
   fCompositeFrame131->SetLayoutManager(new TGVerticalLayout(fCompositeFrame131));

   fCompositeFrame130->AddFrame(fCompositeFrame131, new TGLayoutHints(kLHintsLeft | kLHintsExpandY));

   // canvas widget
   TGCanvas *fCanvas132 = new TGCanvas(fCompositeFrame130,538,323);

   // canvas viewport
   TGViewPort *fViewPort133 = fCanvas132->GetViewPort();

   // canvas container
   Int_t canvasID = gVirtualX->InitWindow((ULong_t)fCanvas132->GetId());
   Window_t winC = gVirtualX->GetWindowID(canvasID);
   TGCompositeFrame *fCompositeFrame142 = new TGCompositeFrame(gClient,winC,fViewPort133);
   fViewPort133->AddFrame(fCompositeFrame142);
   fCompositeFrame142->SetLayoutManager(new TGVerticalLayout(fCompositeFrame142));
   fCompositeFrame142->MapSubwindows();
   fCanvas132->SetContainer(fCompositeFrame142);
   fCanvas132->MapSubwindows();
   fCompositeFrame130->AddFrame(fCanvas132, new TGLayoutHints(kLHintsRight | kLHintsExpandX | kLHintsExpandY));

   fRootCanvas105->AddFrame(fCompositeFrame130, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

   // status bar
   TGStatusBar *fStatusBar145 = new TGStatusBar(fRootCanvas105,10,18);
   Int_t partsusBar145[] = {33,10,10,47};
   fStatusBar145->SetParts(partsusBar145,4);
   fRootCanvas105->AddFrame(fStatusBar145, new TGLayoutHints(kLHintsLeft | kLHintsBottom | kLHintsExpandX,2,2,1,1));

   fCompositeFrame104->AddFrame(fRootCanvas105, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
   fRootCanvas105->Connect("ProcessedConfigure(Event_t*)", 0, 0, "Layout()");

   TGTabElement *tab0 = fTab22->GetTabTab(0);
   tab0->ShowClose(kTRUE);

   // container of "Editor 1"
   TGCompositeFrame *fCompositeFrame153;
   fCompositeFrame153 = fTab22->AddTab("Editor 1");
   fCompositeFrame153->SetLayoutManager(new TGVerticalLayout(fCompositeFrame153));

   // composite frame
   TGCompositeFrame *fTextEditor154 = new TGCompositeFrame(fCompositeFrame153,538,323,kVerticalFrame);
   TGHorizontal3DLine *fHorizontal3DLine167 = new TGHorizontal3DLine(fTextEditor154,538,2);
   fTextEditor154->AddFrame(fHorizontal3DLine167, new TGLayoutHints(kLHintsTop | kLHintsExpandX,0,0,2,2));

   // tool bar
   TGToolBar *fToolBar168 = new TGToolBar(fTextEditor154,538,26,kHorizontalFrame);

   ToolBarData_t t;
   t.fPixmap = "ed_new.png";
   t.fTipText = "New File";
   t.fStayDown = kFALSE;
   t.fId = 1;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   t.fPixmap = "ed_open.png";
   t.fTipText = "Open File";
   t.fStayDown = kFALSE;
   t.fId = 2;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_save.png";
   t.fTipText = "Save File";
   t.fStayDown = kFALSE;
   t.fId = 3;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_saveas.png";
   t.fTipText = "Save File As...";
   t.fStayDown = kFALSE;
   t.fId = 4;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_print.png";
   t.fTipText = "Print";
   t.fStayDown = kFALSE;
   t.fId = 5;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   t.fPixmap = "ed_cut.png";
   t.fTipText = "Cut selection";
   t.fStayDown = kFALSE;
   t.fId = 6;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   TGButton *fPictureButton184 = t.fButton;
   fPictureButton184->SetState(kButtonDisabled);
   t.fPixmap = "ed_copy.png";
   t.fTipText = "Copy selection";
   t.fStayDown = kFALSE;
   t.fId = 7;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   TGButton *fPictureButton187 = t.fButton;
   fPictureButton187->SetState(kButtonDisabled);
   t.fPixmap = "ed_paste.png";
   t.fTipText = "Paste selection";
   t.fStayDown = kFALSE;
   t.fId = 8;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_delete.png";
   t.fTipText = "Delete selection";
   t.fStayDown = kFALSE;
   t.fId = 9;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   TGButton *fPictureButton193 = t.fButton;
   fPictureButton193->SetState(kButtonDisabled);
   t.fPixmap = "ed_find.png";
   t.fTipText = "Find...";
   t.fStayDown = kFALSE;
   t.fId = 10;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   t.fPixmap = "ed_findnext.png";
   t.fTipText = "Find next";
   t.fStayDown = kFALSE;
   t.fId = 11;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_goto.png";
   t.fTipText = "Goto...";
   t.fStayDown = kFALSE;
   t.fId = 12;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_compile.png";
   t.fTipText = "Compile Macro";
   t.fStayDown = kFALSE;
   t.fId = 13;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   t.fPixmap = "ed_execute.png";
   t.fTipText = "Execute Macro";
   t.fStayDown = kFALSE;
   t.fId = 14;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_interrupt.png";
   t.fTipText = "Interrupt";
   t.fStayDown = kFALSE;
   t.fId = 15;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,0);
   t.fPixmap = "ed_help.png";
   t.fTipText = "Help Contents";
   t.fStayDown = kFALSE;
   t.fId = 16;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   t.fPixmap = "ed_quit.png";
   t.fTipText = "Close Editor";
   t.fStayDown = kFALSE;
   t.fId = 17;
   t.fButton = 0;
   fToolBar168->AddButton(fTextEditor154,&t,8);
   TGButton *fPictureButton217 = t.fButton;
   fPictureButton217->SetState(kButtonDisabled);
   fTextEditor154->AddFrame(fToolBar168, new TGLayoutHints(kLHintsTop | kLHintsExpandX));
   TGHorizontal3DLine *fHorizontal3DLine232 = new TGHorizontal3DLine(fTextEditor154,538,2);
   fTextEditor154->AddFrame(fHorizontal3DLine232, new TGLayoutHints(kLHintsTop | kLHintsExpandX,0,0,2,2));
   TGTextEdit *fTextEdit233 = new TGTextEdit(fTextEditor154,538,264);
   fTextEdit233->LoadFile("TxtEdit233");
   fTextEditor154->AddFrame(fTextEdit233, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
   fTextEdit233->Connect("DataDropped(char*)", 0, 0, "DataDropped(char*)");

   // status bar
   TGStatusBar *fStatusBar244 = new TGStatusBar(fTextEditor154,538,18);
   Int_t partsusBar244[] = {75,25};
   fStatusBar244->SetParts(partsusBar244,2);
   fStatusBar244->SetText("Untitled",0);
   fStatusBar244->SetText("Ln 0, Ch 0",1);
   fTextEditor154->AddFrame(fStatusBar244, new TGLayoutHints(kLHintsBottom | kLHintsExpandX,0,0,3,0));

   fCompositeFrame153->AddFrame(fTextEditor154, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
   fTextEditor154->Connect("ProcessedConfigure(Event_t*)", 0, 0, "Layout()");

   TGTabElement *tab1 = fTab22->GetTabTab(1);
   tab1->ShowClose(kTRUE);

   fTab22->SetTab(0);

   fTab22->Resize(fTab22->GetDefaultSize());
   fHorizontalFrame17->AddFrame(fTab22, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));
   fTab22->Connect("CloseTab(int)", 0, 0, "CloseTab(int)");

   fVerticalFrame16->AddFrame(fHorizontalFrame17, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY,2,2,2,2));
   TGHSplitter *fHSplitter24 = new TGHSplitter(fVerticalFrame16,546,4);
   fVerticalFrame16->AddFrame(fHSplitter24, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX));

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame18 = new TGHorizontalFrame(fVerticalFrame16,546,100,kHorizontalFrame | kFixedHeight);

   // tab widget
   TGTab *fTab25 = new TGTab(fHorizontalFrame18,542,96);

   // container of "Command"
   TGCompositeFrame *fCompositeFrame249;
   fCompositeFrame249 = fTab25->AddTab("Command");
   fCompositeFrame249->SetLayoutManager(new TGVerticalLayout(fCompositeFrame249));

   // composite frame
   TGCompositeFrame *fCommandPlugin250 = new TGCompositeFrame(fCompositeFrame249,538,71,kVerticalFrame);

   // horizontal frame
   TGHorizontalFrame *fHorizontalFrame251 = new TGHorizontalFrame(fCommandPlugin250,532,24,kHorizontalFrame);

   gClient->GetColorByName("#ffffff",ucolor);

   // combo box
   TGComboBox *fComboBox252 = new TGComboBox(fHorizontalFrame251,"",1,kHorizontalFrame | kSunkenFrame | kDoubleBorder | kOwnBackground);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out_VV/v25_ZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Ratio.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Ratio.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Ratio.C",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Ratio.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Ratio.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/MjjZll_TEST_7_12/vhbb_TH_Mjj_Zuu_LowPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_Mjj_Zuu_LowPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"vhbb_TH_Mjj_Zee_LowPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/ZllHbb_SR_Datacards_02to1_JECfix_7_3/vhbb_TH_BDT_Zuu_LowPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/ZllHbb_SR_Datacards_02to1_JECfix_7_3/vhbb_TH_BDT_Zuu_LowPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/6_20/VZ/WlnZbb_Datacards_April6_v2_BTFullDecorr_WHFSplit_BDTGT0p2/hists_WmnHighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/6_20/VH/ZnnHbb_Datacards_Jun18_Minus0p8_to_Plus1_NoLowStatShapes/vhbb_TH_Znn_13TeV_Signal.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/6_9/VH_combo090617/ZvvHbb/vhbb_TH_Znn_13TeV_Signal.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/6_9/VH_combo090617/WlvHbb/hists_WenHighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/ZllHbb_Datacards_minCMVAMed_SR0to1_5_25/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/VH_combo220517/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/ZllHbb_Datacards_ZlfMjjCut_5_18/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/ZllHbb_Datacards_ZlfMjjCut_5_18/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out/v25_WZ.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TH1F *hist_1 = new TH1F(\"hist_1\", \"My first histo\", 100, 2, 200);",0);
   fComboBox252->AddEntry(".@",0);
   fComboBox252->AddEntry("TTree* tree=(TTree*)_file0.Get(\"tree)",0);
   fComboBox252->AddEntry(".@",0);
   fComboBox252->AddEntry("TTree* tree=(TTree*)_file0.Get(\"tree);",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_WZ.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ZZ_2L2Q_ext1.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_WZ.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ST_t_antitop.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_WZ.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ST_s.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_WZ.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/VH_combo05052017/ZnnHbb_Datacards_May3/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/VH_combo05052017/ZnnHbb_Datacards_May3/vhbb_TH_Znn_13TeV_TT.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/VH_combo05052017/ZnnHbb_Datacards_May3/vhbb_TH_Znn_13TeV_TT.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"goodBDT/MVA_gg_plus_ZH125_lowZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ST_s.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ST_s.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".aq",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ST_s.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_ttbar.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_gg_plus_ZH125_highZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"MVA_gg_plus_ZH125_lowZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/combo19042017_VH/ZnnHbb_Datacards_WithoutSF_Apr14/vhbb_TH_Znn_13TeV_HighPt_Signal.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/combo19042017_VH/WlnHbb_Datacards_March31/hists_WenHighPt40.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/combo19042017_VH/v25_VH_CMVA_LO_withBjets_4_9/vhbb_TH_Zlf_low_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/combo19042017_VH/v25_VH_CMVA_LO_withBjets_4_9/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/WlnHbb_Datacards_March31/hists_WmnHighPt40.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/v25_VH_CMVA_LO_withBjets_4_9/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/WlnHbb_Datacards_March31/hists_WenHighPt40.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/mlfittest12.root\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/afs/cern.ch/user/d/dcurry/public/shared/datacards/mlfit.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("\\\\.q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".a",0);
   fComboBox252->AddEntry(".aq",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("RooWorkspace",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x fitPtWCorrs.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"Zlf_Vpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"Zlf_Vpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125,ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125,ggZH125.C++",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x Zlf_low_Zuu_Vpt_ZH125,ggZH125.C",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"Zlf_low_Zuu_Vpt_ZH125,ggZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy//files/sys_out/v25_ST_s.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_DY_inclusive.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("MVA_gg_plus_ZH125_highZpt_rejBvsS->Integral(\"width\")",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("gDirectory->cd(\"gg_plus_ZH125_highZpt\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_gg_plus_ZH125_highZpt.root\")",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("gDirectory->cd(\"MVA_gg_plus_ZH125_highZpt\")",0);
   fComboBox252->AddEntry("gDirectory->cd(\"ZllBDT_highptCMVA\")",0);
   fComboBox252->AddEntry("gDirectory->cd(\"Method_BDT\")",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_gg_plus_ZH125_highZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("exit",0);
   fComboBox252->AddEntry("rootls",0);
   fComboBox252->AddEntry("GetListOfFiles()",0);
   fComboBox252->AddEntry("ls()",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("MVA_ZllBDT_lowptCMVA_rejBvsS->Integral(\"width\")",0);
   fComboBox252->AddEntry("Method_BDT->Scan()",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("Method_BDT->cd()",0);
   fComboBox252->AddEntry("Method_BDT-cd()",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("ls",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_gg_plus_ZH125_highZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_gg_plus_ZH125_highZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("gDirectory->pwd()",0);
   fComboBox252->AddEntry("Method_BDT->cd()",0);
   fComboBox252->AddEntry("Method_BDT.cd()",0);
   fComboBox252->AddEntry(".ls",0);
   fComboBox252->AddEntry("gDirectory->pwd()",0);
   fComboBox252->AddEntry("cd MVA_ZllBDT_lowptCMVA_rejBvsS",0);
   fComboBox252->AddEntry("ls()",0);
   fComboBox252->AddEntry("ls",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../data/MVA_VV_bdt_highZpt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_DY_inclusive.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_DY_Bjets_Vpt100to200.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/jec_out/v25_DY_Bjets.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/jec_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/jec_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/jec_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_DY_inclusive.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out_large/v25_DY_inclusive.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_DY_100to200.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/v25_VH_CMVA_LO_3_29/vhbb_TH_BDT_Zee_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ZZ_2L2Q_ext3.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_DY_100to200.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/vtype_out/prep_Zuu_B_ext2.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry(".x VHbbNameSpace.h+",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zee.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_Zuu.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"../limits/v25_VH_CMVA_LO_3_16/vhbb_TH_BDT_Zuu_HighPt.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/prep_out/v25_ZH125.root\")",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_DY_800to1200.root\")",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_DY_800to1200.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_DY_800to1200.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->AddEntry("TBrowser b",0);
   fComboBox252->AddEntry("TFile *_file0 = TFile::Open(\"/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_DY_inclusive.root\")",0);
   fComboBox252->AddEntry(".q",0);
   fComboBox252->Resize(415,22);
   fComboBox252->Select(-1);
   fHorizontalFrame251->AddFrame(fComboBox252, new TGLayoutHints(kLHintsRight | kLHintsCenterY | kLHintsExpandX,5,5,1,1));

   TGFont *ufont;         // will reflect user font changes
   ufont = gClient->GetFont("-*-helvetica-medium-r-*-*-12-*-*-*-*-*-iso8859-1");

   TGGC   *uGC;           // will reflect user GC changes
   // graphics context changes
   GCValues_t vall263;
   vall263.fMask = kGCForeground | kGCBackground | kGCFillStyle | kGCFont | kGCGraphicsExposures;
   gClient->GetColorByName("#000000",vall263.fForeground);
   gClient->GetColorByName("#e0e0e0",vall263.fBackground);
   vall263.fFillStyle = kFillSolid;
   vall263.fFont = ufont->GetFontHandle();
   vall263.fGraphicsExposures = kFALSE;
   uGC = gClient->GetGC(&vall263, kTRUE);
   TGLabel *fLabel263 = new TGLabel(fHorizontalFrame251,"Command (local):",uGC->GetGC());
   fLabel263->SetTextJustify(36);
   fLabel263->SetMargins(0,0,0,0);
   fLabel263->SetWrapLength(-1);
   fHorizontalFrame251->AddFrame(fLabel263, new TGLayoutHints(kLHintsRight | kLHintsCenterY,5,5,1,1));

   fCommandPlugin250->AddFrame(fHorizontalFrame251, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX,3,3,3,3));
   TGTextView *fTextView264 = new TGTextView(fCommandPlugin250,532,35);
   fTextView264->LoadFile("TxtView264");
   fCommandPlugin250->AddFrame(fTextView264, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY,3,3,3,3));

   fCompositeFrame249->AddFrame(fCommandPlugin250, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
   fCommandPlugin250->Connect("ProcessedConfigure(Event_t*)", 0, 0, "Layout()");


   fTab25->SetTab(0);

   fTab25->Resize(fTab25->GetDefaultSize());
   fHorizontalFrame18->AddFrame(fTab25, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY,2,2,2,2));

   fVerticalFrame16->AddFrame(fHorizontalFrame18, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX));
   fHSplitter24->SetFrame(fHorizontalFrame18,kFALSE);

   fHorizontalFrame14->AddFrame(fVerticalFrame16, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));

   fVerticalFrame3->AddFrame(fHorizontalFrame14, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));

   fRootBrowser2->AddFrame(fVerticalFrame3, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX | kLHintsExpandY));

   // status bar
   TGStatusBar *fStatusBar27 = new TGStatusBar(fRootBrowser2,800,18);
   Int_t partsusBar27[] = {33,10,10,47};
   fStatusBar27->SetParts(partsusBar27,4);
   fStatusBar27->SetText("",0);
   fStatusBar27->SetText("",1);
   fStatusBar27->SetText("",2);
   fStatusBar27->SetText("",3);
   fRootBrowser2->AddFrame(fStatusBar27, new TGLayoutHints(kLHintsBottom | kLHintsExpandX));

   fRootBrowser2->SetWindowName("ROOT Object Browser");
   fRootBrowser2->SetIconName("ROOT Object Browser");
   fRootBrowser2->SetIconPixmap("rootdb_s.xpm");
   fRootBrowser2->SetClassHints("ROOT","Browser");
   fRootBrowser2->SetMWMHints(kMWMDecorAll,
                        kMWMFuncAll,
                        kMWMInputModeless);
   fRootBrowser2->SetWMSizeHints(600,350,10000,10000,2,2);
   fRootBrowser2->MapSubwindows();
   fMenuBar160->UnmapWindow();
   fHorizontalFrame13->UnmapWindow();
   fHorizontal3DLine123->UnmapWindow();
   fDockableFrame124->UnmapWindow();
   fHorizontal3DLine129->UnmapWindow();
   fCompositeFrame131->UnmapWindow();
   fStatusBar145->UnmapWindow();

   fRootBrowser2->Resize(fRootBrowser2->GetDefaultSize());
   fRootBrowser2->MapWindow();
   fRootBrowser2->Resize(800,500);
}  

void ToggleSort()
{
   std::cout << "Slot ToggleSort()" << std::endl; 
}

void RequestFilter()
{
   std::cout << "Slot RequestFilter()" << std::endl; 
}

void Refresh()
{
   std::cout << "Slot Refresh()" << std::endl; 
}

void ApplyFilter(int par1)
{
   std::cout << "Slot ApplyFilter(int " << par1 << ")" << std::endl; 
}

void Layout()
{
   std::cout << "Slot Layout()" << std::endl; 
}

void DataDropped(char* par2)
{
   std::cout << "Slot DataDropped(char* " << par2 << ")" << std::endl; 
}

void CloseTab(int par3)
{
   std::cout << "Slot CloseTab(int " << par3 << ")" << std::endl; 
}
