CREATE TABLE "sybaseadmin"."D_PATRON" (
		"PATRONID" "IDENTIFIER" NOT NULL,
	"GeographicID" "SURROGATE_KEY" NOT NULL,
	"GeoDemographicID" "SURROGATE_KEY" NOT NULL,
	"MbrshpID" "SURROGATE_KEY" NOT NULL,
	"ETLJobDtlID" "SURROGATE_KEY" NOT NULL,
	"SignUpSiteID" "SURROGATE_KEY" NOT NULL,
	"HomeSiteID" "SURROGATE_KEY" NOT NULL,
	"SctyCde" "TINY_COUNTER" NULL,
	"PatronNumber" "LEGACY_IDENTIFIER_NUM" NOT NULL,
	"PatronNumberChar" "LEGACY_IDENTIFIER_CHAR" NOT NULL,
	"Mel_LegacyPatronNum" "Legacy_ID_Num_Non_Mandatory" NULL,
	"Mel_LegacyPatronNumChar" "Legacy_ID_Character_Non_Mandatory" NULL,
	"Per_LegacyPatronNum" "Legacy_ID_Num_Non_Mandatory" NULL,
	"Per_LegacyPatronNumChar" "Legacy_ID_Character_Non_Mandatory" NULL,
	"BegEffDt" "FULL_DATE" NOT NULL,
	"EndEffDt" "FULL_DATE" NULL,
	"CurrRowFlg" "FLAG" NOT NULL,
	"ActiveFlg" "FLAG" NULL,
	"PatronSecLvl" "TINY_COUNTER" NULL,
	"Title" "SHORT_NAME" NULL,
	"PatronName" "LONG_NAME" NULL,
	"FirstName" "NAME" NULL,
	"MiddleName" "NAME" NULL,
	"LastName" "NAME" NOT NULL,
	"Suffix" "SHORT_NAME" NULL,
	"Initials" "ABBREVIATION" NULL,
	"Pref_Title" "SHORT_NAME" NULL,
	"Pref_Name" "LONG_NAME" NULL,
	"Pref_FirstName" "NAME" NULL,
	"Pref_MiddleName" "NAME" NULL,
	"Pref_LastName" "NAME" NULL,
	"Pref_Suffix" "SHORT_NAME" NULL,
	"PrefNameFlg" "FLAG" NULL,
	"DOB" "FULL_DATE" NULL,
	"DOB_Yr" "YEAR_NUMBER" NULL,
	"DOB_Mon" "TINY_COUNTER" NULL,
	"DOB_Day" "TINY_COUNTER" NULL,
	"GenderCde" "TYPE_CODE" NULL,
	"Spouse" "LONG_NAME" NULL,
	"OccupationCde" "Medium_Cde" NULL,
	"Occupation" "MEDIUM_DESCRIPTION" NULL,
	"Res_StreetLine1" "STREET_ADDRESS" NULL,
	"Res_StreetLine2" "STREET_ADDRESS" NULL,
	"Res_Suburb" "NAME" NULL,
	"Res_StateCde" "Medium_Cde" NULL,
	"Res_State" "NAME" NULL,
	"Res_CountryCde" "Medium_Cde" NULL,
	"Res_Country" "NAME" NULL,
	"Res_PostCde" "POSTCODE" NULL,
	"Post_StreetLine1" "STREET_ADDRESS" NULL,
	"Post_StreetLine2" "STREET_ADDRESS" NULL,
	"Post_Suburb" "NAME" NULL,
	"Post_StateCde" "Medium_Cde" NULL,
	"Post_State" "NAME" NULL,
	"Post_CountryCde" "Medium_Cde" NULL,
	"Post_Country" "NAME" NULL,
	"Post_PostCde" "POSTCODE" NULL,
	"DT_StreetAddr" "MEDIUM_DESCRIPTION" NULL,
	"DT_Suburb" "NAME" NULL,
	"DT_PostCde" "POSTCODE" NULL,
	"DT_SortPlan" "SORT_PLAN" NULL,
	"DT_StateCde" "ABBREVIATION" NULL,
	"DT_MailBarCde" "MAIL_FULL_BAR_CODE" NULL,
	"DPID" "DPID" NULL,
	"DPID_MatchCmt" "MEDIUM_DESCRIPTION" NULL,
	"LongDegrees" "LONG_LAT" NULL,
	"LatDegrees" "LONG_LAT" NULL,
	"DistanceFrCasino" "SMALL_COUNTER" NULL,
	"HomePhone" "PHONE_NUMBER" NULL,
	"WorkPhone" "PHONE_NUMBER" NULL,
	"AltPhone" "PHONE_NUMBER" NULL,
	"Fax" "PHONE_NUMBER" NULL,
	"MobilePhone" "PHONE_NUMBER" NULL,
	"SMSFlg" "FLAG" NULL,
	"InvalidSMSFlg" "FLAG" NULL,
	"EmailAddr" "EMAIL_ADDRESS" NULL,
	"EmailFlg" "FLAG" NULL,
	"InvalidEmailFlg" "FLAG" NULL,
	"MailToCde" "TYPE_CODE" NULL,
	"MailTo" "SHORT_DESCRIPTION" NULL,
	"MailStsCde" "INDICATOR" NULL,
	"MailSts" "SHORT_DESCRIPTION" NULL,
	"Ethnicity" "NAME" NULL,
	"PrefContactLangCde" "Medium_Cde" NULL,
	"PrefContactLang" "NAME" NULL,
	"CommPref" "SHORT_DESCRIPTION" NULL,
	"Prom_Material_Ind" "SHORT_DESCRIPTION" NULL,
	"GM_Material_Mail_Flg" "FLAG" NULL,
	"Undesirable_Wanted_Ind" "SHORT_DESCRIPTION" NULL,
	"ID_Type" "TYPE_CODE_DESCRIPTION" NULL,
	"ID_Num" "IDENTIFIER_CHARACTER" NULL,
	"ID_ExpiryDt" "FULL_DATE" NULL,
	"ID_IssuStateCde" "Medium_Cde" NULL,
	"ID_IssuState" "NAME" NULL,
	"ID_IssuCountryCde" "Medium_Cde" NULL,
	"ID_IssuCountry" "NAME" NULL,
	"ID_PntsFlg" "FLAG" NULL,
	"SourceCde" "SOURCE_CODE" NULL,
	"SignUpChannel" "SHORT_DESCRIPTION" NULL,
	"SignUpPtyLocNum" "SMALL_COUNTER" NULL,
	"SignUpPty" "NAME" NULL,
	"HomePtyLocNum" "SMALL_COUNTER" NULL,
	"HomePty" "NAME" NULL,
	"ClubJoinDT" "FULL_DATE" NOT NULL,
	"ClubJoinedTmofDy" "TIME_OF_DAY" NULL,
	"SignupCls" "CLASS_TYPE" NULL,
	"Mel_MbrCls" "CLASS_TYPE" NULL,
	"Per_MbrCls" "CLASS_TYPE" NULL,
	"MbrClsGrp" "SHORT_NAME" NULL,
	"ClubType" "TYPE_CODE_DESCRIPTION" NULL,
	"AccntCreationEmpID" "Emp_ID_Long" NULL,
	"ReferredEmpID" "Emp_ID_Long" NULL,
	"PlyrRefer" "Legacy_ID_Num_Non_Mandatory" NULL,
	"YourPlayFlg" "FLAG" NULL,
	"MbrHubAccess" "FLAG" NULL,
	"CrownBetAccnt" "FLAG" NULL,
	"ClubPinFlg" "FLAG" NULL,
	"UnifiedFlg" "FLAG" NULL,
	"UnifiedDt" "FULL_DATE" NULL,
	"UnifiedDtTm" "DATE_AND_TIME" NULL,
	"MigratedFlg" "FLAG" NULL,
	"BusOwnerCde" "Medium_Cde" NULL,
	"BusOwner" "MEDIUM_DESCRIPTION" NULL,
	"PntsBalBand" "BAND_DESCRIPTION" NULL,
	"PriPatronCardFlg" "FLAG" NULL,
	"NumAncillaryCards" "TINY_COUNTER" NULL,
	"JnktOperFlg" "FLAG" NULL,
	"PASOpt" "Short_Cde" NULL,
	"PASDelMethod" "Short_Cde" NULL,
	"PASSignedUpDt" "FULL_DATE" NULL,
	"PASViewedDt" "FULL_DATE" NULL,
	"PASClctdDt" "FULL_DATE" NULL,
	"NetworkName" "SHORT_NAME" NULL,
	"NetworkDesc" "SHORT_DESCRIPTION" NULL,
	"NetworkMbrTyp" "Medium_Catg_Typ_Cde" NULL,
	"CrownLtdID" "Medium_Cde" NULL,
	"CrownLtdName" "MEDIUM_DESCRIPTION" NULL,
	"AddrRgn" "SHORT_NAME" NULL,
	"Country_Metro_Name" "SHORT_NAME" NULL,
	"AddrLocTyp" "SHORT_NAME" NULL,
	"Rgn" "SHORT_NAME" NULL,
	"VIC_Country_Metro_Ind" "INDICATOR" NULL,
	"LGA_Num" "MEDIUM_NUMBER" NULL,
	"LGA_Name" "LONG_NAME" NULL,
	"LGA_Type" "Medium_Cde" NULL,
	"LGA_TypeDesc" "MEDIUM_DESCRIPTION" NULL,
	"T200Flg" "FLAG" NULL,
	"MRMbrFlg" "FLAG" NULL,
	"CmpDrnksAllwdFlg" "FLAG" NULL,
	"BasmntCarParkFlg" "FLAG" NULL,
	"BasmntCarParkFlgAuthEmpID" "Emp_ID_Long" NULL,
	"BasmntCarParkFlgUpdDttm" "DATE_AND_TIME" NULL,
	"ClubLockoutFlg" "FLAG" NULL,
	"ClubLockoutLst" "MEDIUM_DESCRIPTION" NULL,
	"ClubLockoutRsn" "LONG_DESCRIPTION" NULL,
	"PrivLockoutFlg" "FLAG" NULL,
	"PrivLockoutLst" "MEDIUM_DESCRIPTION" NULL,
	"Mel_StopCodes" "STOP_CODE" NULL,
	"Per_StopCodes" "STOP_CODE" NULL,
	"Mel_DailyTmLmtAmt" "SMALL_COUNTER" NULL,
	"Mel_DailyNetLossLmtAmt" "U_Money" NULL,
	"Mel_AnnlNetLossLmtAmt" "U_Money" NULL,
	"Per_DailyTmLmtAmt" "SMALL_COUNTER" NULL,
	"Per_DailyNetLossLmtAmt" "U_Money" NULL,
	"Per_AnnlNetLossLmtAmt" "U_Money" NULL,
	"Mel_PersHostEmpID" "Emp_ID_Long" NULL,
	"Mel_PersHostEmpFirstName" "NAME" NULL,
	"Mel_PersHostEmpLastName" "NAME" NULL,
	"Per_PersHostEmpID" "Emp_ID_Long" NULL,
	"Per_PersHostEmpFirstName" "NAME" NULL,
	"Per_PersHostEmpLastName" "NAME" NULL,
	"MbrshpTyp" "SHORT_NAME" NULL,
	"MbrshpSubTyp" "SHORT_NAME" NULL,
	"MbrshpLvl" "SHORT_NAME" NULL,
	"VIP_ClubLvl" "TINY_COUNTER" NULL,
	"VIP_ClubTagNum" "MEDIUM_NUMBER" NULL,
	"PriPrivCardName" "SHORT_NAME" NULL,
	"ScdryPrivCardName" "SHORT_NAME" NULL,
	"MEL_PatronSegID" "SURROGATE_KEY" NULL,
	"PER_PatronSegID" "SURROGATE_KEY" NULL,
	"ClubLockoutSrc" "SOURCE_CODE" NULL,
	"PrivLockoutSrc" "SOURCE_CODE" NULL,
	"GeographicID_P" "SURROGATE_KEY" NOT NULL,
	"Addr_Valid_Sts_R" "Long_Code" NULL,
	"Addr_Valid_Sts_P" "Long_Code" NULL,
	"DPID_P" "DPID" NULL,
	"DPID_MatchCmt_P" "MEDIUM_DESCRIPTION" NULL,
	"DT_StreetAddr_P" "MEDIUM_DESCRIPTION" NULL,
	"DT_Suburb_P" "NAME" NULL,
	"DT_PostCde_P" "POSTCODE" NULL,
	"DT_SortPlan_P" "SORT_PLAN" NULL,
	"DT_StateCde_P" "ABBREVIATION" NULL,
	"DT_MailBarCde_P" "MAIL_FULL_BAR_CODE" NULL,
	"LongDegrees_P" "LONG_LAT" NULL,
	"LatDegrees_P" "LONG_LAT" NULL,
	"DistanceFrCasino_P" "SMALL_COUNTER" NULL,
	"LGA_Num_P" "MEDIUM_NUMBER" NULL,
	"LGA_Name_P" "LONG_NAME" NULL,
	"LGA_Type_P" "Medium_Cde" NULL,
	"LGA_TypeDesc_P" "MEDIUM_DESCRIPTION" NULL,
	"Email_Typ" "Long_Code" NULL,
	"Email_Valid_Sts" "Long_Code" NULL,
	"Email_Sts_Cde" "Long_Code" NULL,
	"Email_Sts_Des" "LONG_DESCRIPTION" NULL,
	"Email_Dom" "MEDIUM_DESCRIPTION" NULL,
	"Email_Conn" "FLAG" NULL,
	"Email_Disp" "FLAG" NULL,
	"Email_Role_Addr" "FLAG" NULL,
	"Phone_Valid_Sts_M" "Long_Code" NULL,
	"Phone_Sts_Cde_M" "Long_Code" NULL,
	"Phone_Sts_Des_M" "LONG_DESCRIPTION" NULL,
	"Phone_Resp_M" "Long_Code" NULL,
	"Phone_Valid_Sts_H" "Long_Code" NULL,
	"Phone_Sts_Cde_H" "Long_Code" NULL,
	"Phone_Sts_Des_H" "LONG_DESCRIPTION" NULL,
	"Phone_Resp_H" "Long_Code" NULL,
	"Phone_Valid_Sts_W" "Long_Code" NULL,
	"Phone_Sts_Cde_W" "Long_Code" NULL,
	"Phone_Sts_Des_W" "LONG_DESCRIPTION" NULL,
	"Phone_Resp_W" "Long_Code" NULL,
	"Phone_Valid_Sts_O" "Long_Code" NULL,
	"Phone_Sts_Cde_O" "Long_Code" NULL,
	"Phone_Sts_Des_O" "LONG_DESCRIPTION" NULL,
	"Phone_Resp_O" "Long_Code" NULL,
	"SingleNameInd" "FLAG" NULL,
	"CustSts" "Medium_Cde" NULL,
	"MelAdminSts" "LONG_DESCRIPTION" NULL,
	"PerAdminSts" "LONG_DESCRIPTION" NULL,
	"DABInitiatedFlg" "FLAG" NULL,
	"LoyaltyProgram" "NAME" NULL,
	"PriPatronNum" "Legacy_ID_Num_Non_Mandatory" NULL,
	"ScdryAccntRsn" "MEDIUM_DESCRIPTION" NULL,
	"MarketingSiteID" "SURROGATE_KEY" NULL,
	"MarketingPtyLocNum" "SMALL_COUNTER" NULL,
	"MarketingPty" "NAME" NULL,
	"PhoneFlg" CHAR(1) NULL,
	"GFACAckSts" VARCHAR(130) NULL,
	"CoolingOffSts" VARCHAR(130) NULL,
	"CoolingOffStartDtTm" "datetime" NULL,
	"CoolingOffEndDtTm" "datetime" NULL,
	"Syd_StopCodes" VARCHAR(20) NULL,
	"Syd_AdminSts" VARCHAR(255) NULL,
	"Syd_DailyTmLmtAmt" SMALLINT NULL,
	"Syd_DailyNetLossLmtAmt" NUMERIC(18,2) NULL,
	"Syd_HighPrtyCmt" VARCHAR(640) NULL,
	"Syd_PatronSegID" INTEGER NULL,
	"HostEmpID" VARCHAR(10) NULL,
	"HostEmpFirstName" VARCHAR(100) NULL,
	"HostEmpLastName" VARCHAR(100) NULL,
	"HostEmpSiteID" UNSIGNED INT NULL,
	"HostEmpPtyLocNum" SMALLINT NULL,
	"HostEmpPty" VARCHAR(35) NULL,
	"EGMLoyaltyOptInFlg" CHAR(1) NULL,
	PRIMARY KEY ( "PATRONID" ASC )
) IN "IQ_ACTIVE_MAIN";


ALTER TABLE "sybaseadmin"."D_PATRON" ADD PRIMARY KEY ( "PATRONID" ASC );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_ETLJobDtl" NOT NULL FOREIGN KEY ( "ETLJobDtlID" ASC ) REFERENCES "sybaseadmin"."M_ETL_JobDet" ( "ETLJobDtlID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_Geodemographic" NOT NULL FOREIGN KEY ( "GeoDemographicID" ASC ) REFERENCES "sybaseadmin"."D_GeoDemographic" ( "GeoDemographicID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_Geographics" NOT NULL FOREIGN KEY ( "GeographicID" ASC ) REFERENCES "sybaseadmin"."D_Geographics" ( "GeographicID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_Geographics_P" FOREIGN KEY ( "GeographicID_P" ASC ) REFERENCES "sybaseadmin"."D_Geographics" ( "GeographicID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_HomeSite" NOT NULL FOREIGN KEY ( "HomeSiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_Mbrshp" NOT NULL FOREIGN KEY ( "MbrshpID" ASC ) REFERENCES "sybaseadmin"."D_Membership" ( "MbrshpID" );
ALTER TABLE "sybaseadmin"."D_PATRON" ADD CONSTRAINT "FK_Patron_SigUpSite" NOT NULL FOREIGN KEY ( "SignUpSiteID" ASC ) REFERENCES "sybaseadmin"."D_Site" ( "SiteID" );

ALTER TABLE "sybaseadmin"."F_ATS_Jackpot_Hit" ADD CONSTRAINT "FK_ATS_Jkp_Hit_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Consolation_Prize_Transactions" ADD CONSTRAINT "FK_Consolation_Prize_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_DACOM_Bonusing" ADD CONSTRAINT "FK_DACOM_Bonus_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_ExternalRating" ADD CONSTRAINT "FK_ExternalRating_PatronID" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Marketing_Eligibility_History" ADD CONSTRAINT "FK_F_Patron_Marketing_Eligibility_History_Patron" FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Adjustment" ADD CONSTRAINT "FK_F_PromoAdj_Patron" FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_ConfirmeDestPatronID" FOREIGN KEY ( "ConfirmedDestPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_ConfirmedSrcPatronID" FOREIGN KEY ( "ConfirmedSrcPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_Patron" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_TITO_Transactions" ADD CONSTRAINT "FK_F_TITO_Trans_UnconfirmedSrcPatronID" FOREIGN KEY ( "UnconfirmedSrcPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGPATRONMONTH" ADD CONSTRAINT "FK_GamingPatronMonth_Patron" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GCV_Trans" ADD CONSTRAINT "FK_GCVTrans_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Customer_Visits" ADD CONSTRAINT "FK_GuestPatron" NOT NULL FOREIGN KEY ( "GuestPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Customer_Visits" ADD CONSTRAINT "FK_InviterPatron" NOT NULL FOREIGN KEY ( "InviterPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_Hit" ADD CONSTRAINT "FK_Jkpt_Hit_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Jackpot_PatronList" ADD CONSTRAINT "FK_Jkpt_PatronList_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Profile" ADD CONSTRAINT "FK_Key_Plyr_Profile_Jnkt_Patron" NOT NULL FOREIGN KEY ( "JnktOperPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Profile" ADD CONSTRAINT "FK_Key_Plyr_Profile_Key_Plyr_Patron" NOT NULL FOREIGN KEY ( "KeyPlyrPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Mailout_Stream_Event" ADD CONSTRAINT "FK_Mailout_Strm_Evt_Target_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Paging_Alert" ADD CONSTRAINT "FK_PagingAlert_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Parking_Entry_Failure" ADD CONSTRAINT "FK_ParkingEntryFailure_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_ParkingPaymentTransaction" ADD CONSTRAINT "FK_ParkingPayTrans_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_ParkingTransaction" ADD CONSTRAINT "FK_ParkingTrans_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Entry_Management" ADD CONSTRAINT "FK_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Accumulating_Snapshot" ADD CONSTRAINT "FK_Patron_Accumulating_Snapshot" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_Patron_GameRating_PatAncillaryCard" NOT NULL FOREIGN KEY ( "PatronAncillaryCardID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGPATRONHOURGAMEAREA" ADD CONSTRAINT "FK_PATRON_GAMINGPATRONHOURGAMEAREA" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGPATRONVISIT" ADD CONSTRAINT "FK_PATRON_GAMINGPATRONVISIT" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGPATRONVISITGAME" ADD CONSTRAINT "FK_PATRON_GAMINGPATRONVISITGAME" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGPATRONWEEK" ADD CONSTRAINT "FK_PATRON_GAMINGPATRONWEEK" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_GAMINGRATING" ADD CONSTRAINT "FK_PATRON_GAMINGRATING" NOT NULL FOREIGN KEY ( "PATRONID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Membership_CR_Transaction" ADD CONSTRAINT "FK_Patron_MbrshpCRTrans" FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Month_Point_Balance" ADD CONSTRAINT "FK_Patron_Month_Point_Bal_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Interest_Snapshot" ADD CONSTRAINT "FK_Patron_PatronIntrstSnapshot" FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Membership" ADD CONSTRAINT "FK_Patron_PatronMembshp" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Work_Table" ADD CONSTRAINT "FK_Patron_Work_Tbl_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Patron_Recent_Activity" ADD CONSTRAINT "FK_PatronRecentActivity_Patron" NOT NULL FOREIGN KEY ( "PatronId" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Activity" ADD CONSTRAINT "FK_Plyr_Prog_Actvy_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_BACTRACK_Bet_Activity" ADD CONSTRAINT "FK_Plyr_Prog_BT_Bet_Actvy_Jnkt_Patron" NOT NULL FOREIGN KEY ( "JnktOperPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_BACTRACK_Bet_Activity" ADD CONSTRAINT "FK_Plyr_Prog_BT_Bet_Actvy_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Day" ADD CONSTRAINT "FK_Plyr_Prog_Dy_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."D_Plyr_Prog" ADD CONSTRAINT "FK_Plyr_Prog_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Profile" ADD CONSTRAINT "FK_Plyr_Prog_Profile_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Rating" ADD CONSTRAINT "FK_Prog_Key_Plyr_Rating_Jnkt_Patron" NOT NULL FOREIGN KEY ( "JnktOperPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Plyr_Prog_Key_Plyr_Rating" ADD CONSTRAINT "FK_Prog_Key_Plyr_Rating_Patron" NOT NULL FOREIGN KEY ( "KeyPlyrPatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Promotion_Transaction" ADD CONSTRAINT "FK_Promo_Trans_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Survey_Response" ADD CONSTRAINT "FK_Survey_Response_Patron" NOT NULL FOREIGN KEY ( "PatronId" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );
ALTER TABLE "sybaseadmin"."F_Table_Rewards" ADD CONSTRAINT "FK_Tbl_Rewards_Patron" NOT NULL FOREIGN KEY ( "PatronID" ASC ) REFERENCES "sybaseadmin"."D_PATRON" ( "PATRONID" );

CREATE HG INDEX "ASIQ_IDX_T726_C126_HG" ON "sybaseadmin"."D_PATRON" ("MbrshpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T726_C91_HG" ON "sybaseadmin"."D_PATRON" ("GeographicID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T726_C94_HG" ON "sybaseadmin"."D_PATRON" ("GeoDemographicID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T726_I88_HG" ON "sybaseadmin"."D_PATRON" ("PATRONID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T838_C131_HG" ON "sybaseadmin"."D_PATRON" ("ETLJobDtlID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T838_C132_HG" ON "sybaseadmin"."D_PATRON" ("SignUpSiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T838_C133_HG" ON "sybaseadmin"."D_PATRON" ("HomeSiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "ASIQ_IDX_T838_C309_HG" ON "sybaseadmin"."D_PATRON" ("GeographicID_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_AccntCreationEmpID_HG" ON "sybaseadmin"."D_PATRON" ("AccntCreationEmpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ActvFlg_HG" ON "sybaseadmin"."D_PATRON" ("ActiveFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Addr_Valid_Sts_P_HG" ON "sybaseadmin"."D_PATRON" ("Addr_Valid_Sts_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Addr_Valid_Sts_R_HG" ON "sybaseadmin"."D_PATRON" ("Addr_Valid_Sts_R" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_AddrLocTyp_HG" ON "sybaseadmin"."D_PATRON" ("AddrLocTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_AddrRgn_HG" ON "sybaseadmin"."D_PATRON" ("AddrRgn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_BasmntCarParkFlg_HG" ON "sybaseadmin"."D_PATRON" ("BasmntCarParkFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_BasmntCarParkFlgAuthEmpID_HG" ON "sybaseadmin"."D_PATRON" ("BasmntCarParkFlgAuthEmpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DTTM INDEX "IDX_BasmntCarParkFlgUpdDttm_DTTM" ON "sybaseadmin"."D_PATRON" ("BasmntCarParkFlgUpdDttm" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_BegEffDt_DATE" ON "sybaseadmin"."D_PATRON" ("BegEffDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_BegEffDt_HG" ON "sybaseadmin"."D_PATRON" ("BegEffDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_BusOwner_HG" ON "sybaseadmin"."D_PATRON" ("BusOwner" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_BusOwnerCde_HG" ON "sybaseadmin"."D_PATRON" ("BusOwnerCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_ClubJoinDT_DATE" ON "sybaseadmin"."D_PATRON" ("ClubJoinDT" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubJoinDT_HG" ON "sybaseadmin"."D_PATRON" ("ClubJoinDT" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubJoinedTmofDy_HG" ON "sybaseadmin"."D_PATRON" ("ClubJoinedTmofDy" ASC) IN "IQ_ACTIVE_MAIN";
CREATE TIME INDEX "IDX_ClubJoinedTmofDy_Tm" ON "sybaseadmin"."D_PATRON" ("ClubJoinedTmofDy" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubLockoutFlg_HG" ON "sybaseadmin"."D_PATRON" ("ClubLockoutFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubLockoutLst_HG" ON "sybaseadmin"."D_PATRON" ("ClubLockoutLst" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ClubLockoutLst_WD" ON "sybaseadmin"."D_PATRON" ("ClubLockoutLst" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubLockoutRsn_HG" ON "sybaseadmin"."D_PATRON" ("ClubLockoutRsn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ClubLockoutRsn_WD" ON "sybaseadmin"."D_PATRON" ("ClubLockoutRsn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubLockoutSrc_HG" ON "sybaseadmin"."D_PATRON" ("ClubLockoutSrc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HNG INDEX "IDX_ClubLockoutSrc_HNG" ON "sybaseadmin"."D_PATRON" ("ClubLockoutSrc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubPinFlg_HG" ON "sybaseadmin"."D_PATRON" ("ClubPinFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ClubType_HG" ON "sybaseadmin"."D_PATRON" ("ClubType" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_ClubType_WD" ON "sybaseadmin"."D_PATRON" ("ClubType" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CmpDrnksAllwdFlg_HG" ON "sybaseadmin"."D_PATRON" ("CmpDrnksAllwdFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CommPref_HG" ON "sybaseadmin"."D_PATRON" ("CommPref" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CountryMetroName_HG" ON "sybaseadmin"."D_PATRON" ("Country_Metro_Name" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CrownBetAccnt_HG" ON "sybaseadmin"."D_PATRON" ("CrownBetAccnt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CrownLtdID_HG" ON "sybaseadmin"."D_PATRON" ("CrownLtdID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_CrownLtdName_WD" ON "sybaseadmin"."D_PATRON" ("CrownLtdName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CurrRowFlg_HG" ON "sybaseadmin"."D_PATRON" ("CurrRowFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_CustSts_HG" ON "sybaseadmin"."D_PATRON" ("CustSts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DABInitiatedFlg_HG" ON "sybaseadmin"."D_PATRON" ("DABInitiatedFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DistFromCasino_HG" ON "sybaseadmin"."D_PATRON" ("DistanceFrCasino" ASC) IN "IQ_ACTIVE_MAIN";
CREATE LF INDEX "IDX_DistFromCasino_P_LF" ON "sybaseadmin"."D_PATRON" ("DistanceFrCasino_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_DOB_DATE" ON "sybaseadmin"."D_PATRON" ("DOB" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DOB_DAY_HG" ON "sybaseadmin"."D_PATRON" ("DOB_Day" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DOB_HG" ON "sybaseadmin"."D_PATRON" ("DOB" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DOB_MON_HG" ON "sybaseadmin"."D_PATRON" ("DOB_Mon" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DOB_YR_HG" ON "sybaseadmin"."D_PATRON" ("DOB_Yr" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DPID_HG" ON "sybaseadmin"."D_PATRON" ("DPID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DPID_MatchCmt_HG" ON "sybaseadmin"."D_PATRON" ("DPID_MatchCmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DPID_MatchCmt_P_HG" ON "sybaseadmin"."D_PATRON" ("DPID_MatchCmt_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DPID_P_HG" ON "sybaseadmin"."D_PATRON" ("DPID_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_MailBarCde_HG" ON "sybaseadmin"."D_PATRON" ("DT_MailBarCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_MailBarCde_P_HG" ON "sybaseadmin"."D_PATRON" ("DT_MailBarCde_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_PostCde_HG" ON "sybaseadmin"."D_PATRON" ("DT_PostCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_PostCde_P_HG" ON "sybaseadmin"."D_PATRON" ("DT_PostCde_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_SortPlan_HG" ON "sybaseadmin"."D_PATRON" ("DT_SortPlan" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_SortPlan_P_HG" ON "sybaseadmin"."D_PATRON" ("DT_SortPlan_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_StateCde_HG" ON "sybaseadmin"."D_PATRON" ("DT_StateCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_StateCde_P_HG" ON "sybaseadmin"."D_PATRON" ("DT_StateCde_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_DT_StreetAddr_P_WD" ON "sybaseadmin"."D_PATRON" ("DT_StreetAddr_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_DT_StreetAddr_WD" ON "sybaseadmin"."D_PATRON" ("DT_StreetAddr" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_Suburb_HG" ON "sybaseadmin"."D_PATRON" ("DT_Suburb" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_DT_Suburb_P_HG" ON "sybaseadmin"."D_PATRON" ("DT_Suburb_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_EffDt_CMP" ON "sybaseadmin"."D_PATRON" ("BegEffDt" ASC, "EndEffDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Conn_HG" ON "sybaseadmin"."D_PATRON" ("Email_Conn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Disp_HG" ON "sybaseadmin"."D_PATRON" ("Email_Disp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Dom_HG" ON "sybaseadmin"."D_PATRON" ("Email_Dom" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Role_Addr_HG" ON "sybaseadmin"."D_PATRON" ("Email_Role_Addr" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Sts_Cde_HG" ON "sybaseadmin"."D_PATRON" ("Email_Sts_Cde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Sts_Des_HG" ON "sybaseadmin"."D_PATRON" ("Email_Sts_Des" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Typ_HG" ON "sybaseadmin"."D_PATRON" ("Email_Typ" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Email_Valid_Sts_HG" ON "sybaseadmin"."D_PATRON" ("Email_Valid_Sts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_EmailAddr_WD" ON "sybaseadmin"."D_PATRON" ("EmailAddr" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_EmailFlg_HG" ON "sybaseadmin"."D_PATRON" ("EmailFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_EndEffDt_DATE" ON "sybaseadmin"."D_PATRON" ("EndEffDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_EndEffDt_HG" ON "sybaseadmin"."D_PATRON" ("EndEffDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Ethnicity_HG" ON "sybaseadmin"."D_PATRON" ("Ethnicity" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_FirstName_HG" ON "sybaseadmin"."D_PATRON" ("FirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_FirstName_WD" ON "sybaseadmin"."D_PATRON" ("FirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GenderCde_HG" ON "sybaseadmin"."D_PATRON" ("GenderCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_GM_Material_Mail_Flg_HG" ON "sybaseadmin"."D_PATRON" ("GM_Material_Mail_Flg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_HomePhone_WD" ON "sybaseadmin"."D_PATRON" ("HomePhone" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_HomePty_HG" ON "sybaseadmin"."D_PATRON" ("HomePty" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_HomePtyLocNum_HG" ON "sybaseadmin"."D_PATRON" ("HomePtyLocNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_ID_ExpiryDT_DATE" ON "sybaseadmin"."D_PATRON" ("ID_ExpiryDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_ExpiryDT_HG" ON "sybaseadmin"."D_PATRON" ("ID_ExpiryDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_IssuCntry_HG" ON "sybaseadmin"."D_PATRON" ("ID_IssuCountry" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_IssuCntryCde_HG" ON "sybaseadmin"."D_PATRON" ("ID_IssuCountryCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_IssuState_HG" ON "sybaseadmin"."D_PATRON" ("ID_IssuState" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_IssuStateCde_HG" ON "sybaseadmin"."D_PATRON" ("ID_IssuStateCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_Num_HG" ON "sybaseadmin"."D_PATRON" ("ID_Num" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ID_Type_HG" ON "sybaseadmin"."D_PATRON" ("ID_Type" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_IDPntsFlg_HG" ON "sybaseadmin"."D_PATRON" ("ID_PntsFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_InvalidEmailFlg_HG" ON "sybaseadmin"."D_PATRON" ("InvalidEmailFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_InvalidSMSFlg_HG" ON "sybaseadmin"."D_PATRON" ("InvalidSMSFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_JnktOperFlg_HG" ON "sybaseadmin"."D_PATRON" ("JnktOperFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LastName_HG" ON "sybaseadmin"."D_PATRON" ("LastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_LastName_WD" ON "sybaseadmin"."D_PATRON" ("LastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LatDegrees_HG" ON "sybaseadmin"."D_PATRON" ("LatDegrees" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LatDegrees_P_HG" ON "sybaseadmin"."D_PATRON" ("LatDegrees_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_LGAName_P_WD" ON "sybaseadmin"."D_PATRON" ("LGA_Name_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_LGAName_WD" ON "sybaseadmin"."D_PATRON" ("LGA_Name" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGANum_HG" ON "sybaseadmin"."D_PATRON" ("LGA_Num" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGANum_P_HG" ON "sybaseadmin"."D_PATRON" ("LGA_Num_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGAType_HG" ON "sybaseadmin"."D_PATRON" ("LGA_Type" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGAType_P_HG" ON "sybaseadmin"."D_PATRON" ("LGA_Type_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGATypeDesc_HG" ON "sybaseadmin"."D_PATRON" ("LGA_TypeDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LGATypeDesc_P_HG" ON "sybaseadmin"."D_PATRON" ("LGA_TypeDesc_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LongDegrees_HG" ON "sybaseadmin"."D_PATRON" ("LongDegrees" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LongDegrees_P_HG" ON "sybaseadmin"."D_PATRON" ("LongDegrees_P" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_LoyaltyProgram_HG" ON "sybaseadmin"."D_PATRON" ("LoyaltyProgram" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MailSts_HG" ON "sybaseadmin"."D_PATRON" ("MailSts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MailStsCde_HG" ON "sybaseadmin"."D_PATRON" ("MailStsCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MailTo_HG" ON "sybaseadmin"."D_PATRON" ("MailTo" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MailToCde_HG" ON "sybaseadmin"."D_PATRON" ("MailToCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MarketingPty_HG" ON "sybaseadmin"."D_PATRON" ("MarketingPty" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MarketingPtyLocNum_HG" ON "sybaseadmin"."D_PATRON" ("MarketingPtyLocNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MbrClsGrp_HG" ON "sybaseadmin"."D_PATRON" ("MbrClsGrp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MbrHubAccess_HG" ON "sybaseadmin"."D_PATRON" ("MbrHubAccess" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MbrshpLvl_HG" ON "sybaseadmin"."D_PATRON" ("MbrshpLvl" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MbrshpSubTyp_HG" ON "sybaseadmin"."D_PATRON" ("MbrshpSubTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MbrshpTyp_HG" ON "sybaseadmin"."D_PATRON" ("MbrshpTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_AnnlNetLossLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Mel_AnnlNetLossLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_DailyNetLossLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Mel_DailyNetLossLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_DailyTmLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Mel_DailyTmLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_LegacyPatronNum_HG" ON "sybaseadmin"."D_PATRON" ("Mel_LegacyPatronNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_LegacyPatronNumChar_HG" ON "sybaseadmin"."D_PATRON" ("Mel_LegacyPatronNumChar" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_MbrCls_HG" ON "sybaseadmin"."D_PATRON" ("Mel_MbrCls" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MEL_PatronSegID_HG" ON "sybaseadmin"."D_PATRON" ("MEL_PatronSegID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HNG INDEX "IDX_MEL_PatronSegID_HNG" ON "sybaseadmin"."D_PATRON" ("MEL_PatronSegID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_PersHostEmpFirstName_HG" ON "sybaseadmin"."D_PATRON" ("Mel_PersHostEmpFirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Mel_PersHostEmpFirstName_WD" ON "sybaseadmin"."D_PATRON" ("Mel_PersHostEmpFirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_PersHostEmpID_HG" ON "sybaseadmin"."D_PATRON" ("Mel_PersHostEmpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_PersHostEmpLastName_HG" ON "sybaseadmin"."D_PATRON" ("Mel_PersHostEmpLastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Mel_PersHostEmpLastName_WD" ON "sybaseadmin"."D_PATRON" ("Mel_PersHostEmpLastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Mel_StopCodes_HG" ON "sybaseadmin"."D_PATRON" ("Mel_StopCodes" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MelAdminSts_HG" ON "sybaseadmin"."D_PATRON" ("MelAdminSts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MiddleName_HG" ON "sybaseadmin"."D_PATRON" ("MiddleName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MigratedFlg_HG" ON "sybaseadmin"."D_PATRON" ("MigratedFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_MobilePhone_WD" ON "sybaseadmin"."D_PATRON" ("MobilePhone" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_MR_MbrFlg_HG" ON "sybaseadmin"."D_PATRON" ("MRMbrFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NetworkDesc_HG" ON "sybaseadmin"."D_PATRON" ("NetworkDesc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NetworkMbrTyp_HG" ON "sybaseadmin"."D_PATRON" ("NetworkMbrTyp" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NetworkName_HG" ON "sybaseadmin"."D_PATRON" ("NetworkName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_NumAncillaryCards_HG" ON "sybaseadmin"."D_PATRON" ("NumAncillaryCards" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Occupation_HG" ON "sybaseadmin"."D_PATRON" ("Occupation" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_OccupationCde_HG" ON "sybaseadmin"."D_PATRON" ("OccupationCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_PASClctdDt_DATE" ON "sybaseadmin"."D_PATRON" ("PASClctdDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PASClctdDt_HG" ON "sybaseadmin"."D_PATRON" ("PASClctdDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PASDeliveryMethod_HG" ON "sybaseadmin"."D_PATRON" ("PASDelMethod" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PASOpt_HG" ON "sybaseadmin"."D_PATRON" ("PASOpt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_PASSignedUpDt_DATE" ON "sybaseadmin"."D_PATRON" ("PASSignedUpDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PASSignedUpDt_HG" ON "sybaseadmin"."D_PATRON" ("PASSignedUpDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_PASViewedDt_DATE" ON "sybaseadmin"."D_PATRON" ("PASViewedDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PASViewedDt_HG" ON "sybaseadmin"."D_PATRON" ("PASViewedDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Patron_Num_HG" ON "sybaseadmin"."D_PATRON" ("PatronNumber" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PatronName_HG" ON "sybaseadmin"."D_PATRON" ("PatronName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_PatronName_WD" ON "sybaseadmin"."D_PATRON" ("PatronName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PatronNumber_SignUpSiteID_HG" ON "sybaseadmin"."D_PATRON" ("PatronNumber" ASC, "SignUpSiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PatronNumberChar_HG" ON "sybaseadmin"."D_PATRON" ("PatronNumberChar" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PatronSctyLvl_HG" ON "sybaseadmin"."D_PATRON" ("PatronSecLvl" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_AnnlNetLossLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Per_AnnlNetLossLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_DailyNetLossLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Per_DailyNetLossLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_DailyTmLmtAmt_HG" ON "sybaseadmin"."D_PATRON" ("Per_DailyTmLmtAmt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_LegacyPatronNum_HG" ON "sybaseadmin"."D_PATRON" ("Per_LegacyPatronNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_LegacyPatronNumChar_HG" ON "sybaseadmin"."D_PATRON" ("Per_LegacyPatronNumChar" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_MbrCls_HG" ON "sybaseadmin"."D_PATRON" ("Per_MbrCls" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PER_PatronSegID_HG" ON "sybaseadmin"."D_PATRON" ("PER_PatronSegID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_PersHostEmpFirstName_HG" ON "sybaseadmin"."D_PATRON" ("Per_PersHostEmpFirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Per_PersHostEmpFirstName_WD" ON "sybaseadmin"."D_PATRON" ("Per_PersHostEmpFirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_PersHostEmpID_HG" ON "sybaseadmin"."D_PATRON" ("Per_PersHostEmpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_PersHostEmpLastName_HG" ON "sybaseadmin"."D_PATRON" ("Per_PersHostEmpLastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Per_PersHostEmpLastName_WD" ON "sybaseadmin"."D_PATRON" ("Per_PersHostEmpLastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Per_StopCodes_HG" ON "sybaseadmin"."D_PATRON" ("Per_StopCodes" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PerAdminSts_HG" ON "sybaseadmin"."D_PATRON" ("PerAdminSts" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HNG INDEX "IDX_PerthPatronSegID_HNG" ON "sybaseadmin"."D_PATRON" ("PER_PatronSegID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Resp_H_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Resp_H" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Resp_M_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Resp_M" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Resp_O_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Resp_O" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Resp_W_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Resp_W" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Cde_H_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Cde_H" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Cde_M_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Cde_M" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Cde_O_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Cde_O" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Cde_W_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Cde_W" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Des_H_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Des_H" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Des_M_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Des_M" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Des_O_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Des_O" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Sts_Des_W_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Sts_Des_W" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Valid_Sts_H_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Valid_Sts_H" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Valid_Sts_M_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Valid_Sts_M" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Valid_Sts_O_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Valid_Sts_O" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Phone_Valid_Sts_W_HG" ON "sybaseadmin"."D_PATRON" ("Phone_Valid_Sts_W" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PlyrRefer_HG" ON "sybaseadmin"."D_PATRON" ("PlyrRefer" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PntsBalBand_HG" ON "sybaseadmin"."D_PATRON" ("PntsBalBand" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_Country_HG" ON "sybaseadmin"."D_PATRON" ("Post_Country" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_CountryCde_HG" ON "sybaseadmin"."D_PATRON" ("Post_CountryCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_PostCde_HG" ON "sybaseadmin"."D_PATRON" ("Post_PostCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_State_HG" ON "sybaseadmin"."D_PATRON" ("Post_State" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_StateCde_HG" ON "sybaseadmin"."D_PATRON" ("Post_StateCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Post_StrLine1_WD" ON "sybaseadmin"."D_PATRON" ("Post_StreetLine1" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Post_StrLine2_WD" ON "sybaseadmin"."D_PATRON" ("Post_StreetLine2" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Post_Suburb_HG" ON "sybaseadmin"."D_PATRON" ("Post_Suburb" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_PostCde_CMP" ON "sybaseadmin"."D_PATRON" ("Res_PostCde" ASC, "DT_PostCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Pref_FirstName_WD" ON "sybaseadmin"."D_PATRON" ("Pref_FirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Pref_MiddleName_WD" ON "sybaseadmin"."D_PATRON" ("Pref_MiddleName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefContactLang_HG" ON "sybaseadmin"."D_PATRON" ("PrefContactLang" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefContactLangCde_HG" ON "sybaseadmin"."D_PATRON" ("PrefContactLangCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefFirstName_HG" ON "sybaseadmin"."D_PATRON" ("Pref_FirstName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefLastName_HG" ON "sybaseadmin"."D_PATRON" ("Pref_LastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_PrefLastName_WD" ON "sybaseadmin"."D_PATRON" ("Pref_LastName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefMiddleName_HG" ON "sybaseadmin"."D_PATRON" ("Pref_MiddleName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefName_HG" ON "sybaseadmin"."D_PATRON" ("Pref_Name" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_PrefName_WD" ON "sybaseadmin"."D_PATRON" ("Pref_Name" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrefNameFlg_HG" ON "sybaseadmin"."D_PATRON" ("PrefNameFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PriPatronCardFlg_HG" ON "sybaseadmin"."D_PATRON" ("PriPatronCardFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PriPrivCardName_HG" ON "sybaseadmin"."D_PATRON" ("PriPrivCardName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrivLockoutFlg_HG" ON "sybaseadmin"."D_PATRON" ("PrivLockoutFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrivLockoutLst_HG" ON "sybaseadmin"."D_PATRON" ("PrivLockoutLst" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_PrivLockoutLst_WD" ON "sybaseadmin"."D_PATRON" ("PrivLockoutLst" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PrivLockoutSrc_HG" ON "sybaseadmin"."D_PATRON" ("PrivLockoutSrc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HNG INDEX "IDX_PrivLockoutSrc_HNG" ON "sybaseadmin"."D_PATRON" ("PrivLockoutSrc" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_PromMaterialInd_HG" ON "sybaseadmin"."D_PATRON" ("Prom_Material_Ind" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ReferredEmpID_HG" ON "sybaseadmin"."D_PATRON" ("ReferredEmpID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_Country_HG" ON "sybaseadmin"."D_PATRON" ("Res_Country" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_CountryCde_HG" ON "sybaseadmin"."D_PATRON" ("Res_CountryCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_PostCde_HG" ON "sybaseadmin"."D_PATRON" ("Res_PostCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_State_HG" ON "sybaseadmin"."D_PATRON" ("Res_State" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_StateCde_HG" ON "sybaseadmin"."D_PATRON" ("Res_StateCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Res_StrLine1_WD" ON "sybaseadmin"."D_PATRON" ("Res_StreetLine1" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Res_StrLine2_WD" ON "sybaseadmin"."D_PATRON" ("Res_StreetLine2" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Res_Suburb_HG" ON "sybaseadmin"."D_PATRON" ("Res_Suburb" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Rgn_HG" ON "sybaseadmin"."D_PATRON" ("Rgn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ScdryAccntRsn_HG" ON "sybaseadmin"."D_PATRON" ("ScdryAccntRsn" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_ScdryPrivCardName_HG" ON "sybaseadmin"."D_PATRON" ("ScdryPrivCardName" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SctyCde_HG" ON "sybaseadmin"."D_PATRON" ("SctyCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SignUpChannel_HG" ON "sybaseadmin"."D_PATRON" ("SignUpChannel" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SignupCls_HG" ON "sybaseadmin"."D_PATRON" ("SignupCls" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SignUpPty_HG" ON "sybaseadmin"."D_PATRON" ("SignUpPty" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SignUpPtyLocNum_HG" ON "sybaseadmin"."D_PATRON" ("SignUpPtyLocNum" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SingleNameInd_HG" ON "sybaseadmin"."D_PATRON" ("SingleNameInd" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SMSFlg_HG" ON "sybaseadmin"."D_PATRON" ("SMSFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Spouse_HG" ON "sybaseadmin"."D_PATRON" ("Spouse" ASC) IN "IQ_ACTIVE_MAIN";
CREATE WD INDEX "IDX_Spouse_WD" ON "sybaseadmin"."D_PATRON" ("Spouse" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_SrcCde_HG" ON "sybaseadmin"."D_PATRON" ("SourceCde" ASC) IN "IQ_ACTIVE_MAIN";
CREATE CMP INDEX "IDX_Suburb_CMP" ON "sybaseadmin"."D_PATRON" ("Res_Suburb" ASC, "DT_Suburb" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Suffix_HG" ON "sybaseadmin"."D_PATRON" ("Suffix" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_T200Flg_HG" ON "sybaseadmin"."D_PATRON" ("T200Flg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Title_HG" ON "sybaseadmin"."D_PATRON" ("Title" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_Undesirable_Wanted_Ind_HG" ON "sybaseadmin"."D_PATRON" ("Undesirable_Wanted_Ind" ASC) IN "IQ_ACTIVE_MAIN";
CREATE DATE INDEX "IDX_UnifiedDt_DT" ON "sybaseadmin"."D_PATRON" ("UnifiedDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_UnifiedDt_HG" ON "sybaseadmin"."D_PATRON" ("UnifiedDt" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_UnifiedFlg_HG" ON "sybaseadmin"."D_PATRON" ("UnifiedFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE UNIQUE HG INDEX "IDX_UNQ_PatronNumber_BegEffDt_UnifiedFlg_Site_HG" ON "sybaseadmin"."D_PATRON" ("PatronNumber" ASC, "BegEffDt" ASC, "UnifiedFlg" ASC, "SignUpSiteID" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_VICCountryMetroInd_HG" ON "sybaseadmin"."D_PATRON" ("VIC_Country_Metro_Ind" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_VIP_ClubLvl_HG" ON "sybaseadmin"."D_PATRON" ("VIP_ClubLvl" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "IDX_YourPlayFlg_HG" ON "sybaseadmin"."D_PATRON" ("YourPlayFlg" ASC) IN "IQ_ACTIVE_MAIN";
CREATE HG INDEX "PriPatronNum_HG" ON "sybaseadmin"."D_PATRON" ("PriPatronNum" ASC) IN "IQ_ACTIVE_MAIN";

