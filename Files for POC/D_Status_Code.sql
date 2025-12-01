CREATE TABLE "sybaseadmin"."D_Status_Code" (
		"StsID" "SMALL_IDENTIFIER" NOT NULL,
	"StsTyp" "SHORT_DESCRIPTION" NOT NULL,
	"StsCde" "Tiny_Code" NOT NULL,
	"StsDesc" "MEDIUM_DESCRIPTION" NOT NULL,
	CONSTRAINT "PK_D_STATUS_CODE" PRIMARY KEY ( "StsID" ASC )
) IN "IQ_ACTIVE_MAIN";

ALTER TABLE "sybaseadmin"."D_Status_Code" ADD CONSTRAINT "PK_D_STATUS_CODE" PRIMARY KEY ( "StsID" ASC );

ALTER TABLE "sybaseadmin"."F_ATS_Daily_Revenue" ADD CONSTRAINT "FK_ATS_Daily_Rev_Status" NOT NULL FOREIGN KEY ( "PostingStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_ATS_Hourly_Poll" ADD CONSTRAINT "FK_ATS_Hourly_Play_Status" NOT NULL FOREIGN KEY ( "PlayStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_ATS_Hourly_Poll" ADD CONSTRAINT "FK_ATS_Hourly_Poll_Status" NOT NULL FOREIGN KEY ( "PollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_ATS_Jackpot_Configuration" ADD CONSTRAINT "FK_ATS_Jkp_Config_StatusCde" NOT NULL FOREIGN KEY ( "JkptStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_DACOM_Bonusing" ADD CONSTRAINT "FK_Bonus_Awd_Sts" NOT NULL FOREIGN KEY ( "BonusAwdStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Consolation_Prize_Transactions" ADD CONSTRAINT "FK_Consolation_Prize_Status" NOT NULL FOREIGN KEY ( "StsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_FATG_Configuration" ADD CONSTRAINT "FK_F_FATG_Config_Status" NOT NULL FOREIGN KEY ( "FATGStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_Status_Code" NOT NULL FOREIGN KEY ( "TicketLockStId" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_GamingMachine_Configuration" ADD CONSTRAINT "FK_Gaming_Mac_Config_RSG_Sts" NOT NULL FOREIGN KEY ( "RespGamingStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_GamingMachine_Configuration" ADD CONSTRAINT "FK_Gaming_Mac_Config_Sts" NOT NULL FOREIGN KEY ( "MacStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Configuration" ADD CONSTRAINT "FK_Jkpt_Config_Sts" NOT NULL FOREIGN KEY ( "JkptStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_PatronList" ADD CONSTRAINT "FK_Jkpt_PatronList_JkptStsID" NOT NULL FOREIGN KEY ( "JkptStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Daily_Balance" ADD CONSTRAINT "FK_JkptDailyBal_StsCde" NOT NULL FOREIGN KEY ( "PostingStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Schedule" ADD CONSTRAINT "FK_JkptSch_CardedCloseSts" NOT NULL FOREIGN KEY ( "CardedJkptClosePollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Schedule" ADD CONSTRAINT "FK_JkptSch_CardedOpnSts" NOT NULL FOREIGN KEY ( "CardedJkptOpnPollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Schedule" ADD CONSTRAINT "FK_JkptSch_LinkCloseSts" NOT NULL FOREIGN KEY ( "LinkJkptClosePollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Schedule" ADD CONSTRAINT "FK_JkptSch_LinkOpnSts" NOT NULL FOREIGN KEY ( "LinkJkptOpnPollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Machine_Daily_Revenue" ADD CONSTRAINT "FK_Mac_Daily_Rev_Sts" NOT NULL FOREIGN KEY ( "PostingStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Machine_Hourly_Poll" ADD CONSTRAINT "FK_Mac_Hourly_Play_Sts" NOT NULL FOREIGN KEY ( "PlayStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Machine_Hourly_Poll" ADD CONSTRAINT "FK_Mac_Hourly_Poll_Sts" NOT NULL FOREIGN KEY ( "PollStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_POS_Journal_Log" ADD CONSTRAINT "FK_POS_JOURNAL_LOG_JOURNALTYPE" NOT NULL FOREIGN KEY ( "JournalTypeID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_POS_Sale_Line_Item_Transaction" ADD CONSTRAINT "FK_POS_SALE_LI_STATUS_TAXTYP" NOT NULL FOREIGN KEY ( "TaxTypeID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Batch_Transaction" ADD CONSTRAINT "FK_PROMO_BAT_TRANS_STATUS_CODE" NOT NULL FOREIGN KEY ( "PromoTktBatStsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."d_promotion_configuration" ADD CONSTRAINT "FK_PromotionConfiguration_AwardTypID" NOT NULL FOREIGN KEY ( "AwardTypID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Hits" ADD CONSTRAINT "FK_PromotionHits_AwardtypeID" NOT NULL FOREIGN KEY ( "AwardTypID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_Sts_Cde_Gaming_Rating" NOT NULL FOREIGN KEY ( "StsID" ASC ) REFERENCES "sybaseadmin"."D_Status_Code" ( "StsID" );

CREATE HG INDEX "ASIQ_IDX_T1679_I5_HG" ON "sybaseadmin"."D_Status_Code" ("StsID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_StsCde_HG" ON "sybaseadmin"."D_Status_Code" ("StsCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_StsDesc_HG" ON "sybaseadmin"."D_Status_Code" ("StsDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_StsTyp_HG" ON "sybaseadmin"."D_Status_Code" ("StsTyp" ASC) IN "IQ_ACTIVE_MAIN";
