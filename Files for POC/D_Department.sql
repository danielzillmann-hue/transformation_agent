CREATE TABLE "sybaseadmin"."D_Department" (
		"DeptID" "SMALL_IDENTIFIER" NOT NULL,
	"DeptGrp" "Short_Cde" NOT NULL,
	"DeptGrpName" VARCHAR(80) NULL,
	"DeptNum" "DEPARTMENT_LEGACY_ID" NOT NULL,
	"DeptDesc" VARCHAR(70) NULL,
	"SiteID" "SURROGATE_KEY" NOT NULL,
	"SctyCde" "TINY_COUNTER" NULL,
	"ETLJobDtlID" "SURROGATE_KEY" NOT NULL,
	PRIMARY KEY ( "DeptID" ASC )
) IN "IQ_ACTIVE_MAIN";

ALTER TABLE "sybaseadmin"."D_Department" ADD PRIMARY KEY ( "DeptID" ASC );
ALTER TABLE "sybaseadmin"."D_Department" ADD CONSTRAINT "FK_Dept_ETLJobDtl" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."D_Department" ADD CONSTRAINT "FK_Dept_Site" NOT NULL FOREIGN KEY ( "SiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );

ALTER TABLE "sybaseadmin"."F_ExternalRating" ADD CONSTRAINT "FK_ExternalRating_DeptID" NOT NULL FOREIGN KEY ( "DeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );
ALTER TABLE "sybaseadmin"."F_Mailout_Stream_Event" ADD CONSTRAINT "FK_Mailout_Strm_Evt_Mailing_Dept" NOT NULL FOREIGN KEY ( "PromoDeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_BillToDept" NOT NULL FOREIGN KEY ( "BillToDeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Dept" NOT NULL FOREIGN KEY ( "PromoDeptID" ASC ) REFERENCES "sybaseadmin"."D_Department" ( "DeptID" );

CREATE HG INDEX "ASIQ_IDX_T100849_C6_HG" ON "sybaseadmin"."D_Department" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100849_C8_HG" ON "sybaseadmin"."D_Department" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T100849_I9_HG" ON "sybaseadmin"."D_Department" ("DeptID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DeptDesc_HG_UNQ" ON "sybaseadmin"."D_Department" ("DeptDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_DeptDesc_WD" ON "sybaseadmin"."D_Department" ("DeptDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DeptGrp_HG" ON "sybaseadmin"."D_Department" ("DeptGrp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DeptGrpName_HG" ON "sybaseadmin"."D_Department" ("DeptGrpName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE UNIQUE HG INDEX "IDX_DeptNum_HG_UNQ" ON "sybaseadmin"."D_Department" ("DeptNum" ASC, "SiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SctyCde_HG" ON "sybaseadmin"."D_Department" ("SctyCde" ASC) IN "IQ_ACTIVE_MAIN";
