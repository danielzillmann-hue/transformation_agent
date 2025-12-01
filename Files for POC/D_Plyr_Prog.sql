CREATE TABLE "sybaseadmin"."D_Plyr_Prog" (
		"ProgID" UNSIGNED INT NOT NULL,
	"ProgNum" UNSIGNED INT NOT NULL,
	"ProgStartDt" DATE NULL,
	"ProgEndDt" DATE NULL,
	"ProgGrp" VARCHAR(25) NULL,
	"ProgTypCde" CHAR(1) NULL,
	"ProgTypDesc" VARCHAR(15) NULL,
	"ProgCatg" VARCHAR(1024) NULL,
	"ProgCde" VARCHAR(256) NULL,
	"ProgName" VARCHAR(80) NULL,
	"ProgTaxRate" NUMERIC(4,2) NULL,
	"ProgPayTypCde" VARCHAR(5) NULL,
	"ProgPayTypDesc" VARCHAR(30) NULL,
	"ProgTypValCls" VARCHAR(9) NULL,
	"ProgCommRate" NUMERIC(7,4) NULL,
	"ProgCommTOBasis" VARCHAR(30) NULL,
	"ProgCompAllowRate" NUMERIC(7,4) NULL,
	"ProgCompAllowTOBasis" VARCHAR(30) NULL,
	"ProgSts" VARCHAR(64) NULL,
	"ProgRbtTypCde" CHAR(4) NULL,
	"ProgRbtTypDesc" VARCHAR(30) NULL,
	"ProgRbtOnLossPct" NUMERIC(7,4) NULL,
	"ProgEarlyPayCommRate" NUMERIC(7,4) NULL,
	"ProgEarlyPayDiscOnLossPct" NUMERIC(7,4) NULL,
	"ProgRgn" VARCHAR(16) NULL,
	"ProgState" VARCHAR(3) NULL,
	"ProgStateName" VARCHAR(15) NULL,
	"ProgCntry" VARCHAR(3) NULL,
	"ProgCntryName" VARCHAR(50) NULL,
	"ProgOfcCde" VARCHAR(15) NULL,
	"ProgOfcName" VARCHAR(50) NULL,
	"ProgNotes" VARCHAR(255) NULL,
	"PatronID" UNSIGNED INT NOT NULL,
	"DaysProgOpnToDt" SMALLINT NULL,
	"CumulativeCompValEarnedToDt" NUMERIC(19,4) NULL,
	"CumulativeCompValUsedToDt" NUMERIC(19,4) NULL,
	"ProgLastUpdtDt" DATE NULL,
	"PtyLocNum" SMALLINT NULL,
	"PtyLocName" VARCHAR(35) NULL,
	"SiteID" UNSIGNED INT NOT NULL,
	"SctyCde" TINYINT NULL,
	"ETLJobDtlID" UNSIGNED INT NOT NULL,
	"PPPAFlg" VARCHAR(1) NULL,
	"ProgCrcyTyp" VARCHAR(5) NULL,
	"CompRolloverAmt" NUMERIC(19,4) NULL,
	"CompRolloverExpDt" DATE NULL,
	"OpnCompRolloverAmt" NUMERIC(19,4) NULL,
	"PrgPlyrSts" VARCHAR(64) NULL,
	"Segment" VARCHAR(30) NULL,
	CONSTRAINT "PK_D_Plyr_Prog" PRIMARY KEY ( "ProgID" ASC )
) IN "IQ_ACTIVE_MAIN";


ALTER TABLE "sybaseadmin"."D_Plyr_Prog" ADD CONSTRAINT "FK_Plyr_Prog_ETLJobDtl" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."D_Plyr_Prog" ADD CONSTRAINT "FK_Plyr_Prog_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."D_Plyr_Prog" ADD CONSTRAINT "FK_Plyr_Prog_Site" NOT NULL FOREIGN KEY ( "SiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );
ALTER TABLE "sybaseadmin"."D_Plyr_Prog" ADD CONSTRAINT "PK_D_Plyr_Prog" PRIMARY KEY ( "ProgID" ASC );

ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_Gaming_Rating_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_GCV_Trans" ADD CONSTRAINT "FK_GCVTrans_LastKnownProgPlay" NOT NULL FOREIGN KEY ( "LastKnownProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_GCV_Trans" ADD CONSTRAINT "FK_GCVTrans_ProgPlay" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Profile" ADD CONSTRAINT "FK_Key_Plyr_Profile_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Activity" ADD CONSTRAINT "FK_Plyr_Prog_Actvy_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_BACTRACK_Bet_Activity" ADD CONSTRAINT "FK_Plyr_Prog_BT_Bet_Actvy_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Day" ADD CONSTRAINT "FK_Plyr_Prog_Dy_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Profile" ADD CONSTRAINT "FK_Plyr_Prog_Profile_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Rating" ADD CONSTRAINT "FK_Prog_Key_Plyr_Rating_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );
ALTER TABLE "sybaseadmin"."D_Prog_To_Rptg_Grp_Map" ADD CONSTRAINT "FK_Prog_To_Rptg_Grp_Map_Plyr_Prog" NOT NULL FOREIGN KEY ( "ProgID" ASC ) REFERENCES "sybaseadmin"."D_Plyr_Prog" ( "ProgID" );


CREATE HG INDEX "ASIQ_IDX_T100869_C33_HG" ON "sybaseadmin"."D_Plyr_Prog" ("PatronID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100869_C40_HG" ON "sybaseadmin"."D_Plyr_Prog" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100869_C42_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100869_I49_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CompRolloverAmt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("CompRolloverAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_CompRolloverExpDt_DATE" ON "sybaseadmin"."D_Plyr_Prog" ("CompRolloverExpDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_CumulCompEarndUsedToDt_CMP" ON "sybaseadmin"."D_Plyr_Prog" ("CumulativeCompValEarnedToDt" ASC, "CumulativeCompValUsedToDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CumulCompValEarnedToDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("CumulativeCompValEarnedToDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CumulCompValUsedToDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("CumulativeCompValUsedToDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DaysProgOpnToDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("DaysProgOpnToDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_OpnCompRolloverAmt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("OpnCompRolloverAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCatg_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCatg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCntry_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCntry" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCntryName_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCntryName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ProgCntryName_WD" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCntryName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCommRate_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCommRate" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCommTOBasis_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCommTOBasis" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCompAllowRate_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCompAllowRate" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCompAllowTOBasis_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCompAllowTOBasis" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgCrcyTyp_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCrcyTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgDesc_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ProgDesc_WD" ON "sybaseadmin"."D_Plyr_Prog" ("ProgName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgEarlyPayCommRate_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgEarlyPayCommRate" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgEarlyPayDiscOnLossPct_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgEarlyPayDiscOnLossPct" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_ProgEndDt_DATE" ON "sybaseadmin"."D_Plyr_Prog" ("ProgEndDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgEndDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgEndDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgGrp_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgGrp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_ProgLastUpdtDt_DATE" ON "sybaseadmin"."D_Plyr_Prog" ("ProgLastUpdtDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgLastUpdtDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgLastUpdtDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgName_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ProgNotes_WD" ON "sybaseadmin"."D_Plyr_Prog" ("ProgNotes" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgNum_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE UNIQUE HG INDEX "IDX_ProgNum_HG_UNQ" ON "sybaseadmin"."D_Plyr_Prog" ("ProgNum" ASC, "SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgOfcCde_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgOfcCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgOfcName_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgOfcName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ProgOfcName_WD" ON "sybaseadmin"."D_Plyr_Prog" ("ProgOfcName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgPayTypCde_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgPayTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgPayTypDesc_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgPayTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgRbtOnLossPct_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgRbtOnLossPct" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgRbtTypCde_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgRbtTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgRbtTypDesc_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgRbtTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgRgn_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgRgn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_ProgStartDt_DATE" ON "sybaseadmin"."D_Plyr_Prog" ("ProgStartDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgStartDt_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgStartDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_ProgStartEndDt_CMP" ON "sybaseadmin"."D_Plyr_Prog" ("ProgStartDt" ASC, "ProgEndDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgState_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgState" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgStateName_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgStateName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ProgStateName_WD" ON "sybaseadmin"."D_Plyr_Prog" ("ProgStateName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgSts_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgSts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgTaxRate_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgTaxRate" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgTypCde_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgTypDesc_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgTypValCls_HG" ON "sybaseadmin"."D_Plyr_Prog" ("ProgTypValCls" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PtyLocName_HG" ON "sybaseadmin"."D_Plyr_Prog" ("PtyLocName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PtyLocNum_HG" ON "sybaseadmin"."D_Plyr_Prog" ("PtyLocNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SctyCde_HG" ON "sybaseadmin"."D_Plyr_Prog" ("SctyCde" ASC) IN "IQ_ACTIVE_MAIN";
