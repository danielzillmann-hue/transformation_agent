CREATE TABLE "sybaseadmin"."D_GamingLicense" (
		"LicID" "SURROGATE_KEY" NOT NULL,
	"LocTypCde" "Short_Cde" NOT NULL,
	"LocTypDesc" "SHORT_DESCRIPTION" NULL,
	"LicNum" "SHORT_DESCRIPTION" NOT NULL,
	"LicTypCde" "TYPE_CODE" NOT NULL,
	"LicTypDesc" "SHORT_DESCRIPTION" NULL,
	"LicTypGrp" "SHORT_DESCRIPTION" NULL,
	"SiteID" "SURROGATE_KEY" NOT NULL,
	"SctyCde" "TINY_COUNTER" NULL,
	"ETLJobDtlID" "SURROGATE_KEY" NOT NULL,
	CONSTRAINT "PK_D_GAMINGLICENSE" PRIMARY KEY ( "LicID" ASC )
) IN "IQ_ACTIVE_MAIN";

ALTER TABLE "sybaseadmin"."D_GamingLicense" ADD CONSTRAINT "FK_Gaming_Lic_ETLJobDtl" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."D_GamingLicense" ADD CONSTRAINT "FK_Gaming_Lic_Site" NOT NULL FOREIGN KEY ( "SiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );
ALTER TABLE "sybaseadmin"."D_GamingLicense" ADD CONSTRAINT "PK_D_GAMINGLICENSE" PRIMARY KEY ( "LicID" ASC );


ALTER TABLE "sybaseadmin"."F_Bill_Acceptance" ADD CONSTRAINT "FK_Bill_Accept_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Consolation_Prize_Transactions" ADD CONSTRAINT "FK_Consolation_Prize_License" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_DACOM_Bonusing" ADD CONSTRAINT "FK_DACOM_Bonus_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_TITO_Movement_Daily" ADD CONSTRAINT "FK_F_TITO_M_R_TITO_MO_D_LIC" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_GamingMachine_License_Configuration" ADD CONSTRAINT "FK_Gaming_Mac_Lic_Config_License" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_GamingRating_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Hit" ADD CONSTRAINT "FK_Jkpt_Hit_LicID" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Daily_Balance" ADD CONSTRAINT "FK_JkptDailyBal_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Schedule" ADD CONSTRAINT "FK_JkptSch_License" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Machine_Daily_Revenue" ADD CONSTRAINT "FK_Mac_Daily_Rev_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Machine_Hourly_Poll" ADD CONSTRAINT "FK_Mac_Hourly_Poll_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_MacDailyGameRev" ADD CONSTRAINT "FK_MacDailyGameRev_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_MacGameConfigDailySnapshot" ADD CONSTRAINT "FK_MacGameConfigSnapshot_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Activity" ADD CONSTRAINT "FK_Plyr_Prog_Actvy_Lic" NOT NULL FOREIGN KEY ( "LicID" ASC ) REFERENCES "sybaseadmin"."D_GamingLicense" ( "LicID" );


CREATE HG INDEX "ASIQ_IDX_T1808_C10_HG" ON "sybaseadmin"."D_GamingLicense" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T1808_C8_HG" ON "sybaseadmin"."D_GamingLicense" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T1808_I11_HG" ON "sybaseadmin"."D_GamingLicense" ("LicID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LICNUM_HG" ON "sybaseadmin"."D_GamingLicense" ("LicNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LICTYPCDE_HG" ON "sybaseadmin"."D_GamingLicense" ("LicTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LICTYPDESC_HG" ON "sybaseadmin"."D_GamingLicense" ("LicTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LICTYPGRP_HG" ON "sybaseadmin"."D_GamingLicense" ("LicTypGrp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LOCTYPCDE_HG" ON "sybaseadmin"."D_GamingLicense" ("LocTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LOCTYPDESC_HG" ON "sybaseadmin"."D_GamingLicense" ("LocTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SctyCde_HG" ON "sybaseadmin"."D_GamingLicense" ("SctyCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE UNIQUE HG INDEX "IDX_UNQ_LICENSE_HG" ON "sybaseadmin"."D_GamingLicense" ("LocTypCde" ASC, "LicNum" ASC, "LicTypCde" ASC, "SiteID" ASC) IN "IQ_ACTIVE_MAIN";

