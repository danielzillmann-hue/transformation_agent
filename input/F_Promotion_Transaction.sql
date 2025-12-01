CREATE TABLE "sybaseadmin"."F_Promotion_Transaction" (
		"PatronID" UNSIGNED INT NOT NULL,
	"PromoDeptID" SMALLINT NOT NULL,
	"PromoID" UNSIGNED INT NOT NULL,
	"PromoTransDtTm" "datetime" NOT NULL,
	"LegacyAuditStsCde" CHAR(4) NOT NULL,
	"LegacyPromoID" VARCHAR(10) NOT NULL,
	"PromoTransLocID" UNSIGNED INT NOT NULL,
	"PromoTransHrID" UNSIGNED INT NOT NULL,
	"PromoCmtID" UNSIGNED INT NOT NULL,
	"LegacyPatronID" UNSIGNED INT NOT NULL,
	"ActndResourceID" VARCHAR(8) NULL,
	"AuthEmpLicID" VARCHAR(8) NULL,
	"LegacyPromoTyp" CHAR(2) NOT NULL,
	"GenericAuditStsCde" CHAR(4) NOT NULL,
	"ProgNum" UNSIGNED INT NULL,
	"PartRdmdFlg" CHAR(1) NULL,
	"CompletelyRdmdFlg" CHAR(1) NULL,
	"TransCmtFlg" CHAR(1) NOT NULL,
	"PeakRedemptionFlg" CHAR(1) NULL,
	"FaceValDlrAmt" NUMERIC(19,4) NULL,
	"IntTrsfrDlrAmt" NUMERIC(19,4) NULL,
	"NumPnts" NUMERIC(19,4) NULL,
	"ProgID" UNSIGNED INT NOT NULL,
	"ValidCde" SMALLINT NULL,
	"NumCredits" INTEGER NULL,
	"SiteID" UNSIGNED INT NOT NULL,
	"SctyCde" TINYINT NULL,
	"Qty" INTEGER NULL,
	"UnitVal" NUMERIC(18,2) NULL,
	"ETLJobDtlID" UNSIGNED INT NOT NULL,
	"GeneratedbySysCde" CHAR(4) NULL,
	"BillToDeptID" SMALLINT NOT NULL,
	"Cost" NUMERIC(19,4) NULL,
	"Budg" NUMERIC(19,4) NULL,
	"CompType" VARCHAR(32) NULL
) IN "IQ_ACTIVE_MAIN";


ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_BillToDept" NOT NULL FOREIGN KEY ( "BillToDeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Cmt" NOT NULL FOREIGN KEY ( "PromoCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Dept" NOT NULL FOREIGN KEY ( "PromoDeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_ETLJobDtl" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Hr" NOT NULL FOREIGN KEY ( "PromoTransHrID" ASC ) REFERENCES "sybaseadmin"."D_HOUR" ( "HOURID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Loc" NOT NULL FOREIGN KEY ( "PromoTransLocID" ASC ) REFERENCES "sybaseadmin"."D_CASINOLOCATIONDET" ( "CASINOLOCDETID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Site" NOT NULL FOREIGN KEY ( "SiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );


CREATE HG INDEX "ASIQ_IDX_T100859_C1_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PatronID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C2_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoDeptID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C26_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C30_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C32_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("BillToDeptID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C7_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoTransLocID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C8_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoTransHrID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100859_C9_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoCmtID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_ActndAuthEmpLicID_CMP" ON "sybaseadmin"."F_Promotion_Transaction" ("ActndResourceID" ASC, "AuthEmpLicID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ActndResourceID_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("ActndResourceID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_AuthEmpLicID_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("AuthEmpLicID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CompletelyRdmdFlg_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("CompletelyRdmdFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_FaceValDlrAmt_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("FaceValDlrAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GeneratedbySysCde_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("GeneratedbySysCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GenericAuditStsCde_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("GenericAuditStsCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_IntFaceValDlrAmt_CMP" ON "sybaseadmin"."F_Promotion_Transaction" ("IntTrsfrDlrAmt" ASC, "FaceValDlrAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_IntTrsfrDlrAmt_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("IntTrsfrDlrAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Legacy_Patron_ID_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("LegacyPatronID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LegacyAuditStsCde_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("LegacyAuditStsCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LegacyPromoID_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("LegacyPromoID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LegacyPromoID_PromoTyp_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("LegacyPromoID" ASC, "LegacyPromoTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NumCredits_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("NumCredits" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NumPnts_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("NumPnts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PartRdmdFlg_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PartRdmdFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PeakRedemptionFlg_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PeakRedemptionFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ProgNum_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("ProgNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DTTM INDEX "IDX_PromoTransDtTm_DTTM" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoTransDtTm" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PromoTransDtTm_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("PromoTransDtTm" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Qty_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("Qty" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SctyCde_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("SctyCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_TransCmtFlg_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("TransCmtFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_UnitVal_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("UnitVal" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ValidCde_HG" ON "sybaseadmin"."F_Promotion_Transaction" ("ValidCde" ASC) IN "IQ_ACTIVE_MAIN";
