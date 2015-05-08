#include "/user/pvmulder/scripts/tdrstyle.C"

void InputVariables() {
// Example of Root macro based on $ROOTSYS/tutorials/tree/copytree3.C

	setTDRStyle();   

	//Create a new file + a clone of old tree in new file
	TFile *newfile = new TFile("InputVariables.root","recreate");
	TH1F* DiscriminatorJP_B = new TH1F("JP_B","JP_B",100,0,5);
	TH1F* DiscriminatorCSV_B = new TH1F("CSV_B","CSV_B",100,0,1);
	TH1F* DiscriminatorSM_B = new TH1F("SM_B","SM_B",100,0,1);
	TH1F* DiscriminatorSE_B = new TH1F("SE_B","SE_B",100,-0.1,1);
	TH1F* DiscriminatorJP_C = new TH1F("JP_C","JP_C",100,0,5);
	TH1F* DiscriminatorCSV_C = new TH1F("CSV_C","CSV_C",100,0,1);
	TH1F* DiscriminatorSM_C = new TH1F("SM_C","SM_C",100,0,1);
	TH1F* DiscriminatorSE_C = new TH1F("SE_C","SE_C",100,-0.1,1);
	TH1F* DiscriminatorJP_DUSG = new TH1F("JP_DUSG","JP_DUSG",100,0,5);
	TH1F* DiscriminatorCSV_DUSG = new TH1F("CSV_DUSG","CSV_DUSG",100,0,1);
	TH1F* DiscriminatorSM_DUSG = new TH1F("SM_DUSG","SM_DUSG",100,0,1);
	TH1F* DiscriminatorSE_DUSG = new TH1F("SE_DUSG","SE_DUSG",100,-0.1,1);
	TH2F* DiscriminatorNonDefaultJPCSV_B = new TH2F("DiscriminatorNonDefaultJPCSV_B","DiscriminatorNonDefaultJPCSV_B",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSM_B = new TH2F("DiscriminatorNonDefaultJPSM_B","DiscriminatorNonDefaultJPSM_B",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSE_B = new TH2F("DiscriminatorNonDefaultJPSE_B","DiscriminatorNonDefaultJPSE_B",100,0,5,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultCSVSM_B = new TH2F("DiscriminatorNonDefaultCSVSM_B","DiscriminatorNonDefaultCSVSM_B",100,0,1,100,0,1);
	TH2F* DiscriminatorNonDefaultCSVSE_B = new TH2F("DiscriminatorNonDefaultCSVSE_B","DiscriminatorNonDefaultCSVSE_B",100,0,1,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultSMSE_B = new TH2F("DiscriminatorNonDefaultSMSE_B","DiscriminatorNonDefaultSMSE_B",100,0,1,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultJPCSV_C = new TH2F("DiscriminatorNonDefaultJPCSV_C","DiscriminatorNonDefaultJPCSV_C",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSM_C = new TH2F("DiscriminatorNonDefaultJPSM_C","DiscriminatorNonDefaultJPSM_C",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSE_C = new TH2F("DiscriminatorNonDefaultJPSE_C","DiscriminatorNonDefaultJPSE_C",100,0,5,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultCSVSM_C = new TH2F("DiscriminatorNonDefaultCSVSM_C","DiscriminatorNonDefaultCSVSM_C",100,0,1,100,0,1);
	TH2F* DiscriminatorNonDefaultCSVSE_C = new TH2F("DiscriminatorNonDefaultCSVSE_C","DiscriminatorNonDefaultCSVSE_C",100,0,1,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultSMSE_C = new TH2F("DiscriminatorNonDefaultSMSE_C","DiscriminatorNonDefaultSMSE_C",100,0,1,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultJPCSV_DUSG = new TH2F("DiscriminatorNonDefaultJPCSV_DUSG","DiscriminatorNonDefaultJPCSV_DUSG",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSM_DUSG = new TH2F("DiscriminatorNonDefaultJPSM_DUSG","DiscriminatorNonDefaultJPSM_DUSG",100,0,5,100,0,1);
	TH2F* DiscriminatorNonDefaultJPSE_DUSG = new TH2F("DiscriminatorNonDefaultJPSE_DUSG","DiscriminatorNonDefaultJPSE_DUSG",100,0,5,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultCSVSM_DUSG = new TH2F("DiscriminatorNonDefaultCSVSM_DUSG","DiscriminatorNonDefaultCSVSM_DUSG",100,0,1,100,0,1);
	TH2F* DiscriminatorNonDefaultCSVSE_DUSG = new TH2F("DiscriminatorNonDefaultCSVSE_DUSG","DiscriminatorNonDefaultCSVSE_DUSG",100,0,1,100,-0.1,1);
	TH2F* DiscriminatorNonDefaultSMSE_DUSG = new TH2F("DiscriminatorNonDefaultSMSE_DUSG","DiscriminatorNonDefaultSMSE_DUSG",100,0,1,100,-0.1,1);
	TH2F* correlation_B = new TH2F("corrB","corrB",4,0,4,4,0,4);
	TH2F* correlation_C = new TH2F("corrC","corrC",4,0,4,4,0,4);
	TH2F* correlation_DUSG = new TH2F("corrDUSG","corrDUSG",4,0,4,4,0,4);

	TFile *oldfile_b = new TFile("../train_B_save.root");
	TFile *oldfile_c = new TFile("../train_C_save.root");
	TFile *oldfile_dusg = new TFile("../train_DUSG_save.root");
	TTree *treeb = (TTree*)oldfile_b->Get("combinedMVA_save");
	TTree *treec = (TTree*)oldfile_c->Get("combinedMVA_save");
	TTree *treedusg = (TTree*)oldfile_dusg->Get("combinedMVA_save");
	Int_t nentriesb = (Int_t)treeb->GetEntries();
	Int_t nentriesc = (Int_t)treec->GetEntries();
	Int_t nentriesdusg = (Int_t)treedusg->GetEntries();
   
	//Access jet algoDiscriminator to split depending on ntracks
	vector<double>  *algoDiscriminatorb;	
	treeb->SetBranchAddress("algoDiscriminator",&algoDiscriminatorb);
	for (Int_t i=0;i<nentriesb; i++) {
		treeb->GetEntry(i);
		for(int j = 0; j < algoDiscriminatorb->size(); j++){	    
			if(j==0) DiscriminatorJP_B->Fill((*algoDiscriminatorb)[j]);
			if(j==1) DiscriminatorCSV_B->Fill((*algoDiscriminatorb)[j]);
			if(j==2) DiscriminatorSM_B->Fill((*algoDiscriminatorb)[j]);
			if(j==3) DiscriminatorSE_B->Fill((*algoDiscriminatorb)[j]);
		}
//		if((double) (*algoDiscriminatorb)[0]>0.) cout << "JP: " << (*algoDiscriminatorb)[0] << endl;
//		if((double) (*algoDiscriminatorb)[1]>0.) cout << "CSV: " << (*algoDiscriminatorb)[1] << endl;
//		if((double) (*algoDiscriminatorb)[2]>0.) cout << "SM: " << (*algoDiscriminatorb)[2] << endl;
//		if((double) (*algoDiscriminatorb)[3]>0.) cout << "SE: " << (*algoDiscriminatorb)[3] << endl;
		DiscriminatorNonDefaultJPCSV_B->Fill((double)(*algoDiscriminatorb)[0],(double)(*algoDiscriminatorb)[1]);
		DiscriminatorNonDefaultJPSM_B->Fill((double)(*algoDiscriminatorb)[0],(double)(*algoDiscriminatorb)[2]);
		DiscriminatorNonDefaultJPSE_B->Fill((double)(*algoDiscriminatorb)[0],(double)(*algoDiscriminatorb)[3]);
		DiscriminatorNonDefaultCSVSM_B->Fill((double)(*algoDiscriminatorb)[1],(double)(*algoDiscriminatorb)[2]);
		DiscriminatorNonDefaultCSVSE_B->Fill((double)(*algoDiscriminatorb)[1],(double)(*algoDiscriminatorb)[3]);
		DiscriminatorNonDefaultSMSE_B->Fill((double)(*algoDiscriminatorb)[2],(double)(*algoDiscriminatorb)[3]);
	}
	vector<double>  *algoDiscriminatorc;
	treec->SetBranchAddress("algoDiscriminator",&algoDiscriminatorc);
	for (Int_t i=0;i<nentriesc; i++) {
		treec->GetEntry(i);
		for(int j = 0; j < algoDiscriminatorc->size(); j++){	    
			if(j==0) DiscriminatorJP_C->Fill((*algoDiscriminatorc)[j]);
			if(j==1) DiscriminatorCSV_C->Fill((*algoDiscriminatorc)[j]);
			if(j==2) DiscriminatorSM_C->Fill((*algoDiscriminatorc)[j]);
			if(j==3) DiscriminatorSE_C->Fill((*algoDiscriminatorc)[j]);
		}
		DiscriminatorNonDefaultJPCSV_C->Fill((double)(*algoDiscriminatorc)[0],(double)(*algoDiscriminatorc)[1]);
		DiscriminatorNonDefaultJPSM_C->Fill((double)(*algoDiscriminatorc)[0],(double)(*algoDiscriminatorc)[2]);
		DiscriminatorNonDefaultJPSE_C->Fill((double)(*algoDiscriminatorc)[0],(double)(*algoDiscriminatorc)[3]);
		DiscriminatorNonDefaultCSVSM_C->Fill((double)(*algoDiscriminatorc)[1],(double)(*algoDiscriminatorc)[2]);
		DiscriminatorNonDefaultCSVSE_C->Fill((double)(*algoDiscriminatorc)[1],(double)(*algoDiscriminatorc)[3]);
		DiscriminatorNonDefaultSMSE_C->Fill((double)(*algoDiscriminatorc)[2],(double)(*algoDiscriminatorc)[3]);
	}

	vector<double>  *algoDiscriminatordusg;
	treedusg->SetBranchAddress("algoDiscriminator",&algoDiscriminatordusg);
	for (Int_t i=0;i<nentriesdusg; i++) {
		treedusg->GetEntry(i);
		for(int j = 0; j < algoDiscriminatordusg->size(); j++){	    
			if(j==0) DiscriminatorJP_DUSG->Fill((*algoDiscriminatordusg)[j]);
			if(j==1) DiscriminatorCSV_DUSG->Fill((*algoDiscriminatordusg)[j]);
			if(j==2) DiscriminatorSM_DUSG->Fill((*algoDiscriminatordusg)[j]);
			if(j==3) DiscriminatorSE_DUSG->Fill((*algoDiscriminatordusg)[j]);
		}
		DiscriminatorNonDefaultJPCSV_DUSG->Fill((double)(*algoDiscriminatordusg)[0],(double)(*algoDiscriminatordusg)[1]);
		DiscriminatorNonDefaultJPSM_DUSG->Fill((double)(*algoDiscriminatordusg)[0],(double)(*algoDiscriminatordusg)[2]);
		DiscriminatorNonDefaultJPSE_DUSG->Fill((double)(*algoDiscriminatordusg)[0],(double)(*algoDiscriminatordusg)[3]);
		DiscriminatorNonDefaultCSVSM_DUSG->Fill((double)(*algoDiscriminatordusg)[1],(double)(*algoDiscriminatordusg)[2]);
		DiscriminatorNonDefaultCSVSE_DUSG->Fill((double)(*algoDiscriminatordusg)[1],(double)(*algoDiscriminatordusg)[3]);
		DiscriminatorNonDefaultSMSE_DUSG->Fill((double)(*algoDiscriminatordusg)[2],(double)(*algoDiscriminatordusg)[3]);
	}

/*	
	cout << "Correlation factors for B (ignoring the default values, hence based on histogram boundaries):" << endl;
	cout << "Correlation between JP and CSVv2: " << DiscriminatorNonDefaultJPCSV_B->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SM: " << DiscriminatorNonDefaultJPSM_B->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SE: " << DiscriminatorNonDefaultJPSE_B->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SM: " << DiscriminatorNonDefaultCSVSM_B->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SE: " << DiscriminatorNonDefaultCSVSE_B->GetCorrelationFactor()<< endl;
	cout << "Correlation between SM and SE: " << DiscriminatorNonDefaultSMSE_B->GetCorrelationFactor()<< endl;
	cout << "Correlation factors for C (ignoring the default values, hence based on histogram boundaries):" << endl;
	cout << "Correlation between JP and CSVv2: " << DiscriminatorNonDefaultJPCSV_C->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SM: " << DiscriminatorNonDefaultJPSM_C->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SE: " << DiscriminatorNonDefaultJPSE_C->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SM: " << DiscriminatorNonDefaultCSVSM_C->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SE: " << DiscriminatorNonDefaultCSVSE_C->GetCorrelationFactor()<< endl;
	cout << "Correlation between SM and SE: " << DiscriminatorNonDefaultSMSE_C->GetCorrelationFactor()<< endl;
	cout << "Correlation factors for DUSG (ignoring the default values, hence based on histogram boundaries):" << endl;
	cout << "Correlation between JP and CSVv2: " << DiscriminatorNonDefaultJPCSV_DUSG->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SM: " << DiscriminatorNonDefaultJPSM_DUSG->GetCorrelationFactor()<< endl;
	cout << "Correlation between JP and SE: " << DiscriminatorNonDefaultJPSE_DUSG->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SM: " << DiscriminatorNonDefaultCSVSM_DUSG->GetCorrelationFactor()<< endl;
	cout << "Correlation between CSVv2 and SE: " << DiscriminatorNonDefaultCSVSE_DUSG->GetCorrelationFactor()<< endl;
	cout << "Correlation between SM and SE: " << DiscriminatorNonDefaultSMSE_DUSG->GetCorrelationFactor()<< endl;
	*/
	
	correlation_B->SetBinContent(1,1,1);
	correlation_B->SetBinContent(1,2,DiscriminatorNonDefaultJPCSV_B->GetCorrelationFactor());
	correlation_B->SetBinContent(1,3,DiscriminatorNonDefaultJPSM_B->GetCorrelationFactor());
	correlation_B->SetBinContent(1,4,DiscriminatorNonDefaultJPSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(2,1,DiscriminatorNonDefaultJPCSV_B->GetCorrelationFactor());
	correlation_B->SetBinContent(2,2,1);
	correlation_B->SetBinContent(2,3,DiscriminatorNonDefaultCSVSM_B->GetCorrelationFactor());
	correlation_B->SetBinContent(2,4,DiscriminatorNonDefaultCSVSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(3,1,DiscriminatorNonDefaultJPSM_B->GetCorrelationFactor());
	correlation_B->SetBinContent(3,2,DiscriminatorNonDefaultCSVSM_B->GetCorrelationFactor());
	correlation_B->SetBinContent(3,3,1);
	correlation_B->SetBinContent(3,4,DiscriminatorNonDefaultSMSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(4,1,DiscriminatorNonDefaultJPSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(4,2,DiscriminatorNonDefaultCSVSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(4,3,DiscriminatorNonDefaultSMSE_B->GetCorrelationFactor());
	correlation_B->SetBinContent(4,4,1);

  TCanvas *c = new TCanvas("c","c",0,0,600,600);
	correlation_B->SetTitle("");
	correlation_B->SetMarkerSize(2);
	correlation_B->GetXaxis()->SetLabelSize(0.06);
	correlation_B->GetYaxis()->SetLabelSize(0.06);
	correlation_B->GetXaxis()->SetBinLabel(1, "JP");
	correlation_B->GetXaxis()->SetBinLabel(2, "CSVv2");
	correlation_B->GetXaxis()->SetBinLabel(3, "SM");
	correlation_B->GetXaxis()->SetBinLabel(4, "SE");
	correlation_B->GetYaxis()->SetBinLabel(1, "JP");
	correlation_B->GetYaxis()->SetBinLabel(2, "CSVv2");
	correlation_B->GetYaxis()->SetBinLabel(3, "SM");
	correlation_B->GetYaxis()->SetBinLabel(4, "SE");
  gStyle->SetPalette(1);
//  gStyle->SetTitleBorderSize(0);
	gStyle->SetPaintTextFormat("4.2f");
//	gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadRightMargin(0.15);
	correlation_B->Draw("text,colz");
	c->SaveAs("correlation_B.png");

	correlation_C->SetBinContent(1,1,1);
	correlation_C->SetBinContent(1,2,DiscriminatorNonDefaultJPCSV_C->GetCorrelationFactor());
	correlation_C->SetBinContent(1,3,DiscriminatorNonDefaultJPSM_C->GetCorrelationFactor());
	correlation_C->SetBinContent(1,4,DiscriminatorNonDefaultJPSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(2,1,DiscriminatorNonDefaultJPCSV_C->GetCorrelationFactor());
	correlation_C->SetBinContent(2,2,1);
	correlation_C->SetBinContent(2,3,DiscriminatorNonDefaultCSVSM_C->GetCorrelationFactor());
	correlation_C->SetBinContent(2,4,DiscriminatorNonDefaultCSVSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(3,1,DiscriminatorNonDefaultJPSM_C->GetCorrelationFactor());
	correlation_C->SetBinContent(3,2,DiscriminatorNonDefaultCSVSM_C->GetCorrelationFactor());
	correlation_C->SetBinContent(3,3,1);
	correlation_C->SetBinContent(3,4,DiscriminatorNonDefaultSMSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(4,1,DiscriminatorNonDefaultJPSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(4,2,DiscriminatorNonDefaultCSVSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(4,3,DiscriminatorNonDefaultSMSE_C->GetCorrelationFactor());
	correlation_C->SetBinContent(4,4,1);

  TCanvas *cc = new TCanvas("cc","cc",0,0,600,600);
	correlation_C->SetTitle("");
	correlation_C->SetMarkerSize(2);
	correlation_C->GetXaxis()->SetLabelSize(0.06);
	correlation_C->GetYaxis()->SetLabelSize(0.06);
	correlation_C->GetXaxis()->SetBinLabel(1, "JP");
	correlation_C->GetXaxis()->SetBinLabel(2, "CSVv2");
	correlation_C->GetXaxis()->SetBinLabel(3, "SM");
	correlation_C->GetXaxis()->SetBinLabel(4, "SE");
	correlation_C->GetYaxis()->SetBinLabel(1, "JP");
	correlation_C->GetYaxis()->SetBinLabel(2, "CSVv2");
	correlation_C->GetYaxis()->SetBinLabel(3, "SM");
	correlation_C->GetYaxis()->SetBinLabel(4, "SE");
  gStyle->SetPalette(1);
// gStyle->SetTitleBorderSize(0);
	gStyle->SetPaintTextFormat("4.2f");
//	gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadRightMargin(0.15);
	correlation_C->Draw("text,colz");
	cc->SaveAs("correlation_C.png");
	
	correlation_DUSG->SetBinContent(1,1,1);
	correlation_DUSG->SetBinContent(1,2,DiscriminatorNonDefaultJPCSV_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(1,3,DiscriminatorNonDefaultJPSM_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(1,4,DiscriminatorNonDefaultJPSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(2,1,DiscriminatorNonDefaultJPCSV_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(2,2,1);
	correlation_DUSG->SetBinContent(2,3,DiscriminatorNonDefaultCSVSM_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(2,4,DiscriminatorNonDefaultCSVSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(3,1,DiscriminatorNonDefaultJPSM_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(3,2,DiscriminatorNonDefaultCSVSM_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(3,3,1);
	correlation_DUSG->SetBinContent(3,4,DiscriminatorNonDefaultSMSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(4,1,DiscriminatorNonDefaultJPSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(4,2,DiscriminatorNonDefaultCSVSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(4,3,DiscriminatorNonDefaultSMSE_DUSG->GetCorrelationFactor());
	correlation_DUSG->SetBinContent(4,4,1);

  TCanvas *cl= new TCanvas("cl","cl",0,0,600,600);
	correlation_DUSG->SetTitle("");
	correlation_DUSG->SetMarkerSize(2);
	correlation_DUSG->GetXaxis()->SetLabelSize(0.06);
	correlation_DUSG->GetYaxis()->SetLabelSize(0.06);
	correlation_DUSG->GetXaxis()->SetBinLabel(1, "JP");
	correlation_DUSG->GetXaxis()->SetBinLabel(2, "CSVv2");
	correlation_DUSG->GetXaxis()->SetBinLabel(3, "SM");
	correlation_DUSG->GetXaxis()->SetBinLabel(4, "SE");
	correlation_DUSG->GetYaxis()->SetBinLabel(1, "JP");
	correlation_DUSG->GetYaxis()->SetBinLabel(2, "CSVv2");
	correlation_DUSG->GetYaxis()->SetBinLabel(3, "SM");
	correlation_DUSG->GetYaxis()->SetBinLabel(4, "SE");
  gStyle->SetPalette(1);
//  gStyle->SetTitleBorderSize(0);
	gStyle->SetPaintTextFormat("4.2f");
//	gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadRightMargin(0.15);
	correlation_DUSG->Draw("text,colz");
	cl->SaveAs("correlation_DUSG.png");
	
	//plot the histograms!
	//b = red, c = green, light = blue
	TCanvas *c1 = new TCanvas("c1");
	DiscriminatorJP_DUSG->SetTitle("");
	DiscriminatorJP_DUSG->GetXaxis()->SetTitle("discriminator JP");
	DiscriminatorJP_DUSG->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorJP_B->SetLineWidth(2);
	DiscriminatorJP_C->SetLineWidth(2);
	DiscriminatorJP_DUSG->SetLineWidth(2);
	DiscriminatorJP_B->SetLineColor(2);
	DiscriminatorJP_C->SetLineColor(8);
	DiscriminatorJP_DUSG->SetLineColor(4);
	DiscriminatorJP_DUSG->DrawNormalized();		
	DiscriminatorJP_C->DrawNormalized("same");		
	DiscriminatorJP_B->DrawNormalized("same");		
	TLegend* leg = new TLegend(0.65,0.65,0.95,0.9);
	leg->SetFillColor(0);
	leg->AddEntry(DiscriminatorJP_B,"b","L");
	leg->AddEntry(DiscriminatorJP_C,"c","L");
	leg->AddEntry(DiscriminatorJP_DUSG,"dusg","L");
	leg->Draw("SAME");
	c1->SaveAs("DiscriminatorJP.png");

	//b = red, c = green, light = blue
	TCanvas *c2 = new TCanvas("c2");
	DiscriminatorCSV_B->SetTitle("");
	DiscriminatorCSV_B->GetXaxis()->SetTitle("discriminator CSVv2");
	DiscriminatorCSV_B->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorCSV_B->SetLineWidth(2);
	DiscriminatorCSV_C->SetLineWidth(2);
	DiscriminatorCSV_DUSG->SetLineWidth(2);
	DiscriminatorCSV_B->SetLineColor(2);
	DiscriminatorCSV_C->SetLineColor(8);
	DiscriminatorCSV_DUSG->SetLineColor(4);
	DiscriminatorCSV_B->DrawNormalized();		
	DiscriminatorCSV_C->DrawNormalized("same");		
	DiscriminatorCSV_DUSG->DrawNormalized("same");		
	TLegend* leg = new TLegend(0.2,0.65,0.45,0.9);
	leg->SetFillColor(0);
	leg->AddEntry(DiscriminatorCSV_B,"b","L");
	leg->AddEntry(DiscriminatorCSV_C,"c","L");
	leg->AddEntry(DiscriminatorCSV_DUSG,"dusg","L");
	leg->Draw("SAME");
	c2->SaveAs("DiscriminatorCSV.png");

	//b = red, c = green, light = blue
	TCanvas *c3 = new TCanvas("c3");
	DiscriminatorSM_DUSG->SetTitle("");
	DiscriminatorSM_DUSG->GetXaxis()->SetTitle("discriminator SM");
	DiscriminatorSM_DUSG->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorSM_B->SetLineWidth(2);
	DiscriminatorSM_C->SetLineWidth(2);
	DiscriminatorSM_DUSG->SetLineWidth(2);
	DiscriminatorSM_B->SetLineColor(2);
	DiscriminatorSM_C->SetLineColor(8);
	DiscriminatorSM_DUSG->SetLineColor(4);
	DiscriminatorSM_DUSG->DrawNormalized();		
	DiscriminatorSM_C->DrawNormalized("same");		
	DiscriminatorSM_B->DrawNormalized("same");		
	TLegend* leg = new TLegend(0.65,0.65,0.95,0.9);
	leg->SetFillColor(0);
	leg->AddEntry(DiscriminatorSM_B,"b","L");
	leg->AddEntry(DiscriminatorSM_C,"c","L");
	leg->AddEntry(DiscriminatorSM_DUSG,"dusg","L");
	leg->Draw("SAME");
	c3->SaveAs("DiscriminatorSM.png");

	//b = red, c = green, light = blue
	TCanvas *c4 = new TCanvas("c4");
	DiscriminatorSE_DUSG->SetTitle("");
	DiscriminatorSE_DUSG->GetXaxis()->SetTitle("discriminator SE");
	DiscriminatorSE_DUSG->GetXaxis()->SetRangeUser(-0.1,1);
	DiscriminatorSE_B->SetLineWidth(2);
	DiscriminatorSE_C->SetLineWidth(2);
	DiscriminatorSE_DUSG->SetLineWidth(2);
	DiscriminatorSE_B->SetLineColor(2);
	DiscriminatorSE_C->SetLineColor(8);
	DiscriminatorSE_DUSG->SetLineColor(4);
	DiscriminatorSE_DUSG->DrawNormalized();		
	DiscriminatorSE_C->DrawNormalized("same");		
	DiscriminatorSE_B->DrawNormalized("same");		
	TLegend* leg = new TLegend(0.65,0.65,0.95,0.9);
	leg->SetFillColor(0);
	leg->AddEntry(DiscriminatorSE_B,"b","L");
	leg->AddEntry(DiscriminatorSE_C,"c","L");
	leg->AddEntry(DiscriminatorSE_DUSG,"dusg","L");
	leg->Draw("SAME");
	c4->SaveAs("DiscriminatorSE.png");

	newfile->cd();
	DiscriminatorJP_B->Write();
	DiscriminatorCSV_B->Write();
	DiscriminatorSM_B->Write();
	DiscriminatorSE_B->Write();
	DiscriminatorJP_C->Write();
	DiscriminatorCSV_C->Write();
	DiscriminatorSM_C->Write();
	DiscriminatorSE_C->Write();
	DiscriminatorJP_DUSG->Write();
	DiscriminatorCSV_DUSG->Write();
	DiscriminatorSM_DUSG->Write();
	DiscriminatorSE_DUSG->Write();

	DiscriminatorNonDefaultJPCSV_B->Write();
	DiscriminatorNonDefaultJPSM_B->Write();
	DiscriminatorNonDefaultJPSE_B->Write();
	DiscriminatorNonDefaultCSVSM_B->Write();
	DiscriminatorNonDefaultCSVSE_B->Write();
	DiscriminatorNonDefaultSMSE_B->Write();
	DiscriminatorNonDefaultJPCSV_C->Write();
	DiscriminatorNonDefaultJPSM_C->Write();
	DiscriminatorNonDefaultJPSE_C->Write();
	DiscriminatorNonDefaultCSVSM_C->Write();
	DiscriminatorNonDefaultCSVSE_C->Write();
	DiscriminatorNonDefaultSMSE_C->Write();
	DiscriminatorNonDefaultJPCSV_DUSG->Write();
	DiscriminatorNonDefaultJPSM_DUSG->Write();
	DiscriminatorNonDefaultJPSE_DUSG->Write();
	DiscriminatorNonDefaultCSVSM_DUSG->Write();
	DiscriminatorNonDefaultCSVSE_DUSG->Write();
	DiscriminatorNonDefaultSMSE_DUSG->Write();
	
	correlation_B->Write();
	correlation_C->Write();
	correlation_DUSG->Write();

	TCanvas *tcb1 = new TCanvas("tcb1");
	DiscriminatorNonDefaultJPCSV_B->SetTitle("b jets");
//	DiscriminatorNonDefaultJPCSV_B->Add(DiscriminatorNonDefaultJPCSV_C);
//	DiscriminatorNonDefaultJPCSV_B->Add(DiscriminatorNonDefaultJPCSV_B);
	DiscriminatorNonDefaultJPCSV_B->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPCSV_B->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPCSV_B->GetYaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultJPCSV_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPCSV_B->Draw("colz");		
	tcb1->SaveAs("JPvsCSV_B.png");

	TCanvas *tcb2 = new TCanvas("tcb2");
	DiscriminatorNonDefaultJPSM_B->SetTitle("b jets");
//	DiscriminatorNonDefaultJPSM_B->Add(DiscriminatorNonDefaultJPSM_C);
//	DiscriminatorNonDefaultJPSM_B->Add(DiscriminatorNonDefaultJPSM_B);
	DiscriminatorNonDefaultJPSM_B->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSM_B->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSM_B->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultJPSM_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSM_B->Draw("colz");		
	tcb2->SaveAs("JPvsSM_B.png");

	TCanvas *tcb3 = new TCanvas("tcb3");
	DiscriminatorNonDefaultJPSE_B->SetTitle("b jets");
//	DiscriminatorNonDefaultJPSE_B->Add(DiscriminatorNonDefaultJPSE_C);
//	DiscriminatorNonDefaultJPSE_B->Add(DiscriminatorNonDefaultJPSE_B);
	DiscriminatorNonDefaultJPSE_B->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSE_B->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSE_B->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultJPSE_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSE_B->Draw("colz");		
	tcb3->SaveAs("JPvsSE_B.png");

	TCanvas *tcb4 = new TCanvas("tcb4");
	DiscriminatorNonDefaultCSVSM_B->SetTitle("b jets");
//	DiscriminatorNonDefaultCSVSM_B->Add(DiscriminatorNonDefaultCSVSM_C);
//	DiscriminatorNonDefaultCSVSM_B->Add(DiscriminatorNonDefaultCSVSM_B);
	DiscriminatorNonDefaultCSVSM_B->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSM_B->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_B->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultCSVSM_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_B->Draw("colz");		
	tcb4->SaveAs("CSVvsSM_B.png");

	TCanvas *tcb5 = new TCanvas("tcb5");
	DiscriminatorNonDefaultCSVSE_B->SetTitle("b jets");
//	DiscriminatorNonDefaultCSVSE_B->Add(DiscriminatorNonDefaultCSVSE_C);
//	DiscriminatorNonDefaultCSVSE_B->Add(DiscriminatorNonDefaultCSVSE_B);
	DiscriminatorNonDefaultCSVSE_B->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSE_B->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_B->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultCSVSE_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_B->Draw("colz");		
	tcb5->SaveAs("CSVvsSE_B.png");

	TCanvas *tcb6 = new TCanvas("tcb6");
	DiscriminatorNonDefaultSMSE_B->SetTitle("b jets");
//	DiscriminatorNonDefaultSMSE_B->Add(DiscriminatorNonDefaultSMSE_C);
//	DiscriminatorNonDefaultSMSE_B->Add(DiscriminatorNonDefaultSMSE_B);
	DiscriminatorNonDefaultSMSE_B->GetXaxis()->SetTitle("SM");
	DiscriminatorNonDefaultSMSE_B->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_B->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultSMSE_B->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_B->Draw("colz");		
	tcb6->SaveAs("SMvsSE_B.png");


	TCanvas *tcc1 = new TCanvas("tcc1");
	DiscriminatorNonDefaultJPCSV_C->SetTitle("c jets");
//	DiscriminatorNonDefaultJPCSV_C->Add(DiscriminatorNonDefaultJPCSV_C);
//	DiscriminatorNonDefaultJPCSV_C->Add(DiscriminatorNonDefaultJPCSV_B);
	DiscriminatorNonDefaultJPCSV_C->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPCSV_C->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPCSV_C->GetYaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultJPCSV_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPCSV_C->Draw("colz");		
	tcc1->SaveAs("JPvsCSV_C.png");

	TCanvas *tcc2 = new TCanvas("tcc2");
	DiscriminatorNonDefaultJPSM_C->SetTitle("c jets");
//	DiscriminatorNonDefaultJPSM_C->Add(DiscriminatorNonDefaultJPSM_C);
//	DiscriminatorNonDefaultJPSM_C->Add(DiscriminatorNonDefaultJPSM_B);
	DiscriminatorNonDefaultJPSM_C->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSM_C->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSM_C->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultJPSM_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSM_C->Draw("colz");		
	tcc2->SaveAs("JPvsSM_C.png");

	TCanvas *tcc3 = new TCanvas("tcc3");
	DiscriminatorNonDefaultJPSE_C->SetTitle("c jets");
//	DiscriminatorNonDefaultJPSE_C->Add(DiscriminatorNonDefaultJPSE_C);
//	DiscriminatorNonDefaultJPSE_C->Add(DiscriminatorNonDefaultJPSE_B);
	DiscriminatorNonDefaultJPSE_C->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSE_C->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSE_C->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultJPSE_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSE_C->Draw("colz");		
	tcc3->SaveAs("JPvsSE_C.png");

	TCanvas *tcc4 = new TCanvas("tcc4");
	DiscriminatorNonDefaultCSVSM_C->SetTitle("c jets");
//	DiscriminatorNonDefaultCSVSM_C->Add(DiscriminatorNonDefaultCSVSM_C);
//	DiscriminatorNonDefaultCSVSM_C->Add(DiscriminatorNonDefaultCSVSM_B);
	DiscriminatorNonDefaultCSVSM_C->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSM_C->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_C->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultCSVSM_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_C->Draw("colz");		
	tcc4->SaveAs("CSVvsSM_C.png");

	TCanvas *tcc5 = new TCanvas("tcc5");
	DiscriminatorNonDefaultCSVSE_C->SetTitle("c jets");
//	DiscriminatorNonDefaultCSVSE_C->Add(DiscriminatorNonDefaultCSVSE_C);
//	DiscriminatorNonDefaultCSVSE_C->Add(DiscriminatorNonDefaultCSVSE_B);
	DiscriminatorNonDefaultCSVSE_C->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSE_C->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_C->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultCSVSE_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_C->Draw("colz");		
	tcc5->SaveAs("CSVvsSE_C.png");

	TCanvas *tcc6 = new TCanvas("tcc6");
	DiscriminatorNonDefaultSMSE_C->SetTitle("c jets");
//	DiscriminatorNonDefaultSMSE_C->Add(DiscriminatorNonDefaultSMSE_C);
//	DiscriminatorNonDefaultSMSE_C->Add(DiscriminatorNonDefaultSMSE_B);
	DiscriminatorNonDefaultSMSE_C->GetXaxis()->SetTitle("SM");
	DiscriminatorNonDefaultSMSE_C->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_C->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultSMSE_C->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_C->Draw("colz");		
	tcc6->SaveAs("SMvsSE_C.png");


	TCanvas *tcl1 = new TCanvas("tcl1");
	DiscriminatorNonDefaultJPCSV_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultJPCSV_DUSG->Add(DiscriminatorNonDefaultJPCSV_C);
//	DiscriminatorNonDefaultJPCSV_DUSG->Add(DiscriminatorNonDefaultJPCSV_B);
	DiscriminatorNonDefaultJPCSV_DUSG->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPCSV_DUSG->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPCSV_DUSG->GetYaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultJPCSV_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPCSV_DUSG->Draw("colz");		
	tcl1->SaveAs("JPvsCSV_DUSG.png");

	TCanvas *tcl2 = new TCanvas("tcl2");
	DiscriminatorNonDefaultJPSM_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultJPSM_DUSG->Add(DiscriminatorNonDefaultJPSM_C);
//	DiscriminatorNonDefaultJPSM_DUSG->Add(DiscriminatorNonDefaultJPSM_B);
	DiscriminatorNonDefaultJPSM_DUSG->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSM_DUSG->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSM_DUSG->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultJPSM_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSM_DUSG->Draw("colz");		
	tcl2->SaveAs("JPvsSM_DUSG.png");

	TCanvas *tcl3 = new TCanvas("tcl3");
	DiscriminatorNonDefaultJPSE_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultJPSE_DUSG->Add(DiscriminatorNonDefaultJPSE_C);
//	DiscriminatorNonDefaultJPSE_DUSG->Add(DiscriminatorNonDefaultJPSE_B);
	DiscriminatorNonDefaultJPSE_DUSG->GetXaxis()->SetTitle("JP");
	DiscriminatorNonDefaultJPSE_DUSG->GetXaxis()->SetRangeUser(0,5);
	DiscriminatorNonDefaultJPSE_DUSG->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultJPSE_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultJPSE_DUSG->Draw("colz");		
	tcl3->SaveAs("JPvsSE_DUSG.png");

	TCanvas *tcl4 = new TCanvas("tcl4");
	DiscriminatorNonDefaultCSVSM_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultCSVSM_DUSG->Add(DiscriminatorNonDefaultCSVSM_C);
//	DiscriminatorNonDefaultCSVSM_DUSG->Add(DiscriminatorNonDefaultCSVSM_B);
	DiscriminatorNonDefaultCSVSM_DUSG->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSM_DUSG->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_DUSG->GetYaxis()->SetTitle("SM");
	DiscriminatorNonDefaultCSVSM_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSM_DUSG->Draw("colz");		
	tcl4->SaveAs("CSVvsSM_DUSG.png");

	TCanvas *tcl5 = new TCanvas("tcl5");
	DiscriminatorNonDefaultCSVSE_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultCSVSE_DUSG->Add(DiscriminatorNonDefaultCSVSE_C);
//	DiscriminatorNonDefaultCSVSE_DUSG->Add(DiscriminatorNonDefaultCSVSE_B);
	DiscriminatorNonDefaultCSVSE_DUSG->GetXaxis()->SetTitle("CSVv2");
	DiscriminatorNonDefaultCSVSE_DUSG->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_DUSG->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultCSVSE_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultCSVSE_DUSG->Draw("colz");		
	tcl5->SaveAs("CSVvsSE_DUSG.png");

	TCanvas *tcl6 = new TCanvas("tcl6");
	DiscriminatorNonDefaultSMSE_DUSG->SetTitle("dusg jets");
//	DiscriminatorNonDefaultSMSE_DUSG->Add(DiscriminatorNonDefaultSMSE_C);
//	DiscriminatorNonDefaultSMSE_DUSG->Add(DiscriminatorNonDefaultSMSE_B);
	DiscriminatorNonDefaultSMSE_DUSG->GetXaxis()->SetTitle("SM");
	DiscriminatorNonDefaultSMSE_DUSG->GetXaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_DUSG->GetYaxis()->SetTitle("SE");
	DiscriminatorNonDefaultSMSE_DUSG->GetYaxis()->SetRangeUser(0,1);
	DiscriminatorNonDefaultSMSE_DUSG->Draw("colz");		
	tcl6->SaveAs("SMvsSE_DUSG.png");

 
	newfile->Close();

}
