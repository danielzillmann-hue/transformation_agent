CREATE TABLE "sybaseadmin"."D_jackpot_product_type" (
		"JkptProdTypID" "SURROGATE_KEY" NOT NULL,
	"SiteID" "SURROGATE_KEY" NOT NULL,
	"SctyCde" "TINY_COUNTER" NOT NULL,
	"ETLJobDtlID" "SURROGATE_KEY" NOT NULL,
	"JkptProdTyp" "LONG_NAME" NOT NULL,
	"JkptProdTypOrder" "SMALL_COUNTER" NULL,
	CONSTRAINT "PK_D_jackpot_product_type" PRIMARY KEY ( "JkptProdTypID" ASC )
) IN "IQ_ACTIVE_MAIN";

ALTER TABLE "sybaseadmin"."D_jackpot_product_type" ADD CONSTRAINT "PK_D_jackpot_product_type" PRIMARY KEY ( "JkptProdTypID" ASC );

ALTER TABLE "sybaseadmin"."F_Machine_Daily_Revenue" ADD CONSTRAINT "FK_Mac_Daily_Rev_JkptProdTyp" NOT NULL FOREIGN KEY ( "JkptProdTypID" ASC ) REFERENCES "sybaseadmin"."D_jackpot_product_type" ( "JkptProdTypID" );
ALTER TABLE "sybaseadmin"."F_Machine_Hourly_Poll" ADD CONSTRAINT "FK_Mac_Hourly_Poll_JkptProdTyp" NOT NULL FOREIGN KEY ( "JkptProdTypID" ASC ) REFERENCES "sybaseadmin"."D_jackpot_product_type" ( "JkptProdTypID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_Patron_GameRating_JkptProdType" NOT NULL FOREIGN KEY ( "JkptProdTypID" ASC ) REFERENCES "sybaseadmin"."D_jackpot_product_type" ( "JkptProdTypID" );

CREATE HG INDEX "ASIQ_IDX_T21490_I7_HG" ON "sybaseadmin"."D_jackpot_product_type" ("JkptProdTypID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ETLJobDtlID_HG" ON "sybaseadmin"."D_jackpot_product_type" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_JkptProdTyp_WD" ON "sybaseadmin"."D_jackpot_product_type" ("JkptProdTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_JkptProdTypOrder_HG" ON "sybaseadmin"."D_jackpot_product_type" ("JkptProdTypOrder" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SiteID_HG" ON "sybaseadmin"."D_jackpot_product_type" ("SiteID" ASC) IN "IQ_ACTIVE_MAIN";
