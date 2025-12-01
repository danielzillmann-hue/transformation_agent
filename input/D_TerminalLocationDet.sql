CREATE TABLE "sybaseadmin"."D_TerminalLocationDet" (
		"TerminalLocationDetID" "SURROGATE_KEY" NOT NULL,
	"CASINOLOCDETID" "IDENTIFIER" NOT NULL,
	"TerminalLoc" "Terminal_Location" NULL,
	"CASINOLOC" "CASINO_LOCATION" NOT NULL,
	"PITNUM" "LOCATION_SUB_CODE" NULL,
	"GamingTableNum" "LOCATION_SUB_CODE" NOT NULL,
	"TerminalNum" "LOCATION_SUB_CODE" NULL,
	"TBLAREA" "TABLE_AREA_LOCATION" NULL,
	"CasinoLocDesc" "MEDIUM_DESCRIPTION" NULL,
	"GAMINGAREA" "TYPE_CODE" NULL,
	"GamingAreaName" "SHORT_NAME" NULL,
	"GamingAreaStrm" "SHORT_NAME" NULL,
	"GamingAreaSeg" "SHORT_NAME" NULL,
	"GamingAreaSubSeg" "SHORT_NAME" NULL,
	"NumSGStns" "TINY_COUNTER" NULL,
	"SiteID" "SURROGATE_KEY" NOT NULL,
	"SctyCde" "TINY_COUNTER" NULL,
	"ETLJobDtlID" "SURROGATE_KEY" NOT NULL,
	"PagingZone" "MEDIUM_DESCRIPTION" NULL,
	CONSTRAINT "PK_D_TERMINALLOCATIONDET" PRIMARY KEY ( "TerminalLocationDetID" ASC )
) IN "IQ_ACTIVE_MAIN";

ALTER TABLE "sybaseadmin"."D_TerminalLocationDet" ADD CONSTRAINT "FK_D_TerminalLocationDet_CasinoLocationDet" NOT NULL FOREIGN KEY ( "CASINOLOCDETID" ASC ) REFERENCES "sybaseadmin"."D_CASINOLOCATIONDET" ( "CASINOLOCDETID" );
ALTER TABLE "sybaseadmin"."D_TerminalLocationDet" ADD CONSTRAINT "FK_D_TerminalLocationDet_ETLJobDet" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."D_TerminalLocationDet" ADD CONSTRAINT "FK_D_TerminalLocationDet_Site" NOT NULL FOREIGN KEY ( "SiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );
ALTER TABLE "sybaseadmin"."D_TerminalLocationDet" ADD CONSTRAINT "PK_D_TERMINALLOCATIONDET" PRIMARY KEY ( "TerminalLocationDetID" ASC );

ALTER TABLE "sybaseadmin"."F_ATS_Daily_Revenue" ADD CONSTRAINT "FK_ATS_Daily_Rev_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_ATS_Hourly_Poll" ADD CONSTRAINT "FK_ATS_Hourly_Poll_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_ATS_Jackpot_Configuration" ADD CONSTRAINT "FK_ATS_Jkp_Config_TermLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_ATS_Jackpot_Hit" ADD CONSTRAINT "FK_ATS_Jkp_Hit_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_FATG_Configuration" ADD CONSTRAINT "FK_F_FATG_Config_TerminalDet" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_TITO_Movement_Monthly" ADD CONSTRAINT "FK_F_TITO_M_R_TITO_MO_D_TERMIN" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_TITO_Movement_Daily" ADD CONSTRAINT "FK_F_TITO_M_R_TITO_MO_D_TERMIN" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_TerminalLocDet" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_GamingRating_TerminallocDtl" FOREIGN KEY ( "Terminallocationdetid" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Hit" ADD CONSTRAINT "FK_Jkpt_Hit_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Daily_Balance" ADD CONSTRAINT "FK_JkptDailyBal_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_Paging_Alert" ADD CONSTRAINT "FK_PagingAlert_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );
ALTER TABLE "sybaseadmin"."F_Paging_Transaction" ADD CONSTRAINT "FK_PagingTransaction_TerminalLoc" NOT NULL FOREIGN KEY ( "TerminalLocationDetID" ASC ) REFERENCES "sybaseadmin"."D_TerminalLocationDet" ( "TerminalLocationDetID" );

CREATE HG INDEX "ASIQ_IDX_T1639_C16_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T1639_C18_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T1639_C2_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("CASINOLOCDETID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T1639_I19_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("TerminalLocationDetID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CasinoLoc_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("CASINOLOC" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CasinoLocDesc_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("CasinoLocDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GamingArea_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("GAMINGAREA" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GamingAreaName_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("GamingAreaName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_GamingAreaName_WD" ON "sybaseadmin"."D_TerminalLocationDet" ("GamingAreaName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GamingAreaStrm_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("GamingAreaStrm" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GamingAreaSubSeg_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("GamingAreaSubSeg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GamingTabNum_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("GamingTableNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NumSGStns_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("NumSGStns" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PagingZone_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("PagingZone" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PitNum_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("PITNUM" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_TBLAREA_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("TBLAREA" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_TerminalLoc_HG" ON "sybaseadmin"."D_TerminalLocationDet" ("TerminalLoc" ASC) IN "IQ_ACTIVE_MAIN";

