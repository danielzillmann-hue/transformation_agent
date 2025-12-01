CREATE TABLE "sybaseadmin"."D_Comment" (
		"CmtID" UNSIGNED INT NOT NULL,
	"CmtTypCde" CHAR(2) NOT NULL,
	"CmtTypDesc" VARCHAR(30) NOT NULL,
	"CmtDesc" VARCHAR(130) NOT NULL,
	"ETLJobDtlID" UNSIGNED INT NOT NULL,
	CONSTRAINT "PK_D_Comment" PRIMARY KEY ( "CmtID" ASC )
) IN "IQ_ACTIVE_MAIN";


ALTER TABLE "sybaseadmin"."D_Comment" ADD CONSTRAINT "PK_D_Comment" PRIMARY KEY ( "CmtID" ASC );

ALTER TABLE "sybaseadmin"."F_Membership_CR_Transaction" ADD CONSTRAINT "FK_Cmt_MbrshpCRTrans" NOT NULL FOREIGN KEY ( "RsnCdeID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Adjustment" ADD CONSTRAINT "FK_F_PromoAdj_Cmt" FOREIGN KEY ( "AdjCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Customer_Visits" ADD CONSTRAINT "FK_GstVstLmtOvrrdeCmt" NOT NULL FOREIGN KEY ( "GstVstLmtOvrrdeCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Customer_Visits" ADD CONSTRAINT "FK_LiaisonGstLmtOvrrdeCmt" NOT NULL FOREIGN KEY ( "LiaisonGstLmtOvrrdeCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_ParkingCashFlow" ADD CONSTRAINT "FK_ParkingCshFlow_Cmt" NOT NULL FOREIGN KEY ( "CmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Parking_Entry_Failure" ADD CONSTRAINT "FK_ParkingEntryFailure_Cmt" NOT NULL FOREIGN KEY ( "CmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_ParkingSystemEvent" ADD CONSTRAINT "FK_ParkingSystEvt_Cmt" NOT NULL FOREIGN KEY ( "CmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_POS_Check" ADD CONSTRAINT "FK_POS_CHECK_COMMENT" NOT NULL FOREIGN KEY ( "CheckCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_POS_Sale_Line_Item_Transaction" ADD CONSTRAINT "FK_POS_SALE_LI_CHK_CMT" NOT NULL FOREIGN KEY ( "CheckCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_POS_Sale_Line_Item_Transaction" ADD CONSTRAINT "FK_POS_SALE_LI_LI_CMT" NOT NULL FOREIGN KEY ( "LineItemCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Cmt" NOT NULL FOREIGN KEY ( "PromoCmtID" ASC ) REFERENCES "sybaseadmin"."D_Comment" ( "CmtID" );


CREATE HG INDEX "ASIQ_IDX_T100856_I6_HG" ON "sybaseadmin"."D_Comment" ("CmtID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_CmtDesc_WD" ON "sybaseadmin"."D_Comment" ("CmtDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CmtTypCde_HG" ON "sybaseadmin"."D_Comment" ("CmtTypCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CmtTypDesc_HG" ON "sybaseadmin"."D_Comment" ("CmtTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_CmtTypDesc_WD" ON "sybaseadmin"."D_Comment" ("CmtTypDesc" ASC) IN "IQ_ACTIVE_MAIN";
