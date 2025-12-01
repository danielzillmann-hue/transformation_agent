# Data Categorization Report

## Identified Business Domains

### Customer & Loyalty Management
Manages patron profiles, demographics, membership details, and player loyalty programs. Includes information on patron age groups, geographic and demographic segments, and program participation.

### Casino Operations & Locations
Defines the physical and organizational structure of casino sites, gaming areas (pits, EGM areas), detailed location breakdowns (banks, machines, tables), and internal departments.

### Gaming Products & Assets
Catalogs gaming equipment (machines, manufacturers, models), specific game offerings, their features, denominations, and associated jackpot types. Covers the inventory of what's available for play.

### Gaming Activity & Performance
Captures detailed records of gaming sessions, patron ratings, and various transaction types related to gaming. This domain is central to analyzing player engagement and operational performance.

### Promotions & Marketing
Tracks promotional campaigns, special offers to patrons, and the transactions associated with these marketing activities.

### Regulatory & Compliance
Contains information regarding various gaming licenses, their types, descriptions, and regulatory compliance requirements for casino operations.

### Reference & Time Data
Provides universal time dimensions (hours, days, weeks, months), general lookup/status codes, and comment types for operational support and consistent reporting across other domains.

## Categorization Statistics

- **Total Tables Categorized**: 19
- **Total Fields Categorized**: 661

### Fields per Domain

- **Customer & Loyalty Management**: 258 fields
- **Reference & Time Data**: 140 fields
- **Casino Operations & Locations**: 114 fields
- **Gaming Products & Assets**: 50 fields
- **Regulatory & Compliance**: 47 fields
- **Gaming Activity & Performance**: 35 fields
- **Promotions & Marketing**: 17 fields

## Table Categorizations

### D_AGE

| Field | Domain |
|-------|--------|
| AGE | Customer & Loyalty Management |
| AGEBAND | Customer & Loyalty Management |
| AGEID | Customer & Loyalty Management |
| SctyCde | Reference & Time Data |
| SiteID | Casino Operations & Locations |

### D_CASINOLOCATION

| Field | Domain |
|-------|--------|
| CASINOLOCID | Casino Operations & Locations |
| EGM_AREA | Casino Operations & Locations |
| ETLJobDtlID | Reference & Time Data |
| GAMINGAREA | Casino Operations & Locations |
| LOCTYPCODE | Casino Operations & Locations |
| PITNUM | Casino Operations & Locations |
| SctyCde | Casino Operations & Locations |
| SiteID | Casino Operations & Locations |

### D_Comment

| Field | Domain |
|-------|--------|
| CmtDesc | Reference & Time Data |
| CmtID | Reference & Time Data |
| CmtTypCde | Reference & Time Data |
| CmtTypDesc | Reference & Time Data |
| ETLJobDtlID | Reference & Time Data |

### D_Department

| Field | Domain |
|-------|--------|
| DeptDesc | Casino Operations & Locations |
| DeptGrp | Casino Operations & Locations |
| DeptGrpName | Casino Operations & Locations |
| DeptID | Casino Operations & Locations |
| DeptNum | Casino Operations & Locations |
| ETLJobDtlID | Reference & Time Data |
| SctyCde | Reference & Time Data |
| SiteID | Casino Operations & Locations |

### D_GAMINGMACHINE

| Field | Domain |
|-------|--------|
| DEVICEID | Gaming Products & Assets |
| ETLJobDtlID | Reference & Time Data |
| GAMINGMACHINEID | Gaming Products & Assets |
| MACMODELNAME | Gaming Products & Assets |
| MACTYP | Gaming Products & Assets |
| MANUFCODE | Gaming Products & Assets |
| MANUFNAME | Gaming Products & Assets |
| MacModelGrp | Gaming Products & Assets |
| MacModelGrpName | Gaming Products & Assets |
| MacTypName | Gaming Products & Assets |
| MaxBillDenomAccepted | Gaming Products & Assets |
| PAI | Gaming Products & Assets |
| SERIALNUM | Gaming Products & Assets |
| SctyCde | Reference & Time Data |
| SiteID | Casino Operations & Locations |
| TicketInFlg | Gaming Products & Assets |
| TicketOutFlg | Gaming Products & Assets |

### D_GamingLicense

| Field | Domain |
|-------|--------|
| ETLJobDtlID | Reference & Time Data |
| LicID | Regulatory & Compliance |
| LicNum | Regulatory & Compliance |
| LicTypCde | Regulatory & Compliance |
| LicTypDesc | Regulatory & Compliance |
| LicTypGrp | Regulatory & Compliance |
| LocTypCde | Regulatory & Compliance |
| LocTypDesc | Regulatory & Compliance |
| SctyCde | Regulatory & Compliance |
| SiteID | Casino Operations & Locations |

### D_HOUR

| Field | Domain |
|-------|--------|
| AUSPUBHLDYFLG | Reference & Time Data |
| AUSPUBHLDYNAME | Reference & Time Data |
| CLNDRYRNAME | Reference & Time Data |
| CLNDRYRNUM | Reference & Time Data |
| DAYBEFOREAUSPUBHLDYFLG | Reference & Time Data |
| DAYBEFOREVICPUBHLDYFLG | Reference & Time Data |
| DAYID | Reference & Time Data |
| DAYNAME | Reference & Time Data |
| DAYNUMCLNDRYR | Reference & Time Data |
| DAYNUMFISCALYR | Reference & Time Data |
| DAYNUMMON | Reference & Time Data |
| DAYNUMQTR | Reference & Time Data |
| DAYNUMWK | Reference & Time Data |
| DAYSHORTNAME | Reference & Time Data |
| DAYSSINCE30_06_1994 | Reference & Time Data |
| DTNOTYETFLG | Reference & Time Data |
| DayBreakdown | Reference & Time Data |
| EightHrBandDesc | Reference & Time Data |
| EightHrBandNum | Reference & Time Data |
| FISCALYRNAME | Reference & Time Data |
| FISCALYRNUM | Reference & Time Data |
| FOURHOURBANDDESC | Reference & Time Data |
| FOURHOURBANDNUM | Reference & Time Data |
| FULLDT | Reference & Time Data |
| FinQtrByWk | Reference & Time Data |
| FinQtrByWkLbl | Reference & Time Data |
| FinYrHalf | Reference & Time Data |
| FinYrHalfByWk | Reference & Time Data |
| FullClndrDtDesc | Reference & Time Data |
| GAMINGHOURDESC | Reference & Time Data |
| GAMINGHOURNUMWITHINDAY | Reference & Time Data |
| HOURDESC | Reference & Time Data |
| HOURID | Reference & Time Data |
| HOURNUMWITHINDAY | Reference & Time Data |
| HOURSSINCE30_06_1994 | Reference & Time Data |
| HrGrpDesc | Reference & Time Data |
| INTLPUBHLDYCNTRYNAME | Reference & Time Data |
| INTLPUBHLDYFLG | Reference & Time Data |
| INTLPUBHLDYNAME | Reference & Time Data |
| LASTDAYINCLNDRYRFLG | Reference & Time Data |
| LASTDAYINFISCALYRFLG | Reference & Time Data |
| LASTDAYINMONFLG | Reference & Time Data |
| LASTDAYINQTRFLG | Reference & Time Data |
| LEAPYRFLG | Reference & Time Data |
| MONTHENDDT | Reference & Time Data |
| MONTHID | Reference & Time Data |
| MONTHNAME | Reference & Time Data |
| MONTHNUMINCLNDRYR | Reference & Time Data |
| MONTHNUMINFISCALYR | Reference & Time Data |
| MONTHNUMINQTR | Reference & Time Data |
| MONTHSHORTNAME | Reference & Time Data |
| MONTHSTARTDT | Reference & Time Data |
| NUMDAYSINMON | Reference & Time Data |
| PEAKDAYFLG | Reference & Time Data |
| PEAKHOURIND | Reference & Time Data |
| PREVCLNDRMONNUM | Reference & Time Data |
| PREVCLNDRQTRLBL | Reference & Time Data |
| PREVCLNDRQTRNUM | Reference & Time Data |
| PREVFISCALMONNUM | Reference & Time Data |
| PREVFISCALQTRLBL | Reference & Time Data |
| PREVFISCALQTRNUM | Reference & Time Data |
| PREVMONNAME | Reference & Time Data |
| PREVMONSHORTNAME | Reference & Time Data |
| PUBHLDYWKFLG | Reference & Time Data |
| QTRLBLCLNDRYR | Reference & Time Data |
| QTRLBLFISCALYR | Reference & Time Data |
| QTRNUMCLNDRYR | Reference & Time Data |
| QTRNUMFISCALYR | Reference & Time Data |
| RELATIVEGAMINGDAY | Reference & Time Data |
| ROLLCURR4WKFLG | Reference & Time Data |
| ROLLQTRINDBYMON | Reference & Time Data |
| ROLLYRINDBYMON | Reference & Time Data |
| ROLLYRINDBYWK | Reference & Time Data |
| RelativeGamingMonth | Reference & Time Data |
| RelativeGamingWk | Reference & Time Data |
| SCHLHLDYWKFLG | Reference & Time Data |
| SEASONNAME | Reference & Time Data |
| SPCLEVNTWKFLG | Reference & Time Data |
| THREEHOURBANDDESC | Reference & Time Data |
| THREEHOURBANDNUM | Reference & Time Data |
| VICPUBHLDYFLG | Reference & Time Data |
| VICPUBHLDYNAME | Reference & Time Data |
| VICSCHLHLDYFLG | Reference & Time Data |
| WEEKID | Reference & Time Data |
| WHOLEWKSSINCE27_06_1994 | Reference & Time Data |
| WKENDDT | Reference & Time Data |
| WKNUMCLNDRYR | Reference & Time Data |
| WKNUMFISCALYR | Reference & Time Data |
| WKSTARTDT | Reference & Time Data |
| WeekdayRange | Reference & Time Data |
| YearID | Reference & Time Data |

### D_PATRON

| Field | Domain |
|-------|--------|
| AccntCreationEmpID | Customer & Loyalty Management |
| ActiveFlg | Customer & Loyalty Management |
| AddrLocTyp | Customer & Loyalty Management |
| AddrRgn | Customer & Loyalty Management |
| Addr_Valid_Sts_P | Customer & Loyalty Management |
| Addr_Valid_Sts_R | Customer & Loyalty Management |
| AltPhone | Customer & Loyalty Management |
| BasmntCarParkFlg | Customer & Loyalty Management |
| BasmntCarParkFlgAuthEmpID | Customer & Loyalty Management |
| BasmntCarParkFlgUpdDttm | Reference & Time Data |
| BegEffDt | Reference & Time Data |
| BusOwner | Casino Operations & Locations |
| BusOwnerCde | Casino Operations & Locations |
| ClubJoinDT | Customer & Loyalty Management |
| ClubJoinedTmofDy | Customer & Loyalty Management |
| ClubLockoutFlg | Regulatory & Compliance |
| ClubLockoutLst | Regulatory & Compliance |
| ClubLockoutRsn | Regulatory & Compliance |
| ClubLockoutSrc | Regulatory & Compliance |
| ClubPinFlg | Customer & Loyalty Management |
| ClubType | Customer & Loyalty Management |
| CmpDrnksAllwdFlg | Customer & Loyalty Management |
| CommPref | Customer & Loyalty Management |
| CoolingOffEndDtTm | Regulatory & Compliance |
| CoolingOffStartDtTm | Regulatory & Compliance |
| CoolingOffSts | Regulatory & Compliance |
| Country_Metro_Name | Customer & Loyalty Management |
| CrownBetAccnt | Customer & Loyalty Management |
| CrownLtdID | Casino Operations & Locations |
| CrownLtdName | Casino Operations & Locations |
| CurrRowFlg | Reference & Time Data |
| CustSts | Customer & Loyalty Management |
| DABInitiatedFlg | Customer & Loyalty Management |
| DOB | Customer & Loyalty Management |
| DOB_Day | Customer & Loyalty Management |
| DOB_Mon | Customer & Loyalty Management |
| DOB_Yr | Customer & Loyalty Management |
| DPID | Customer & Loyalty Management |
| DPID_MatchCmt | Customer & Loyalty Management |
| DPID_MatchCmt_P | Customer & Loyalty Management |
| DPID_P | Customer & Loyalty Management |
| DT_MailBarCde | Customer & Loyalty Management |
| DT_MailBarCde_P | Customer & Loyalty Management |
| DT_PostCde | Customer & Loyalty Management |
| DT_PostCde_P | Customer & Loyalty Management |
| DT_SortPlan | Customer & Loyalty Management |
| DT_SortPlan_P | Customer & Loyalty Management |
| DT_StateCde | Customer & Loyalty Management |
| DT_StateCde_P | Customer & Loyalty Management |
| DT_StreetAddr | Customer & Loyalty Management |
| DT_StreetAddr_P | Customer & Loyalty Management |
| DT_Suburb | Customer & Loyalty Management |
| DT_Suburb_P | Customer & Loyalty Management |
| DistanceFrCasino | Customer & Loyalty Management |
| DistanceFrCasino_P | Customer & Loyalty Management |
| EGMLoyaltyOptInFlg | Customer & Loyalty Management |
| ETLJobDtlID | Reference & Time Data |
| EmailAddr | Customer & Loyalty Management |
| EmailFlg | Customer & Loyalty Management |
| Email_Conn | Customer & Loyalty Management |
| Email_Disp | Customer & Loyalty Management |
| Email_Dom | Customer & Loyalty Management |
| Email_Role_Addr | Customer & Loyalty Management |
| Email_Sts_Cde | Customer & Loyalty Management |
| Email_Sts_Des | Customer & Loyalty Management |
| Email_Typ | Customer & Loyalty Management |
| Email_Valid_Sts | Customer & Loyalty Management |
| EndEffDt | Reference & Time Data |
| Ethnicity | Customer & Loyalty Management |
| Fax | Customer & Loyalty Management |
| FirstName | Customer & Loyalty Management |
| GFACAckSts | Regulatory & Compliance |
| GM_Material_Mail_Flg | Promotions & Marketing |
| GenderCde | Customer & Loyalty Management |
| GeoDemographicID | Customer & Loyalty Management |
| GeographicID | Customer & Loyalty Management |
| GeographicID_P | Customer & Loyalty Management |
| HomePhone | Customer & Loyalty Management |
| HomePty | Casino Operations & Locations |
| HomePtyLocNum | Casino Operations & Locations |
| HomeSiteID | Casino Operations & Locations |
| HostEmpFirstName | Customer & Loyalty Management |
| HostEmpID | Customer & Loyalty Management |
| HostEmpLastName | Customer & Loyalty Management |
| HostEmpPty | Casino Operations & Locations |
| HostEmpPtyLocNum | Casino Operations & Locations |
| HostEmpSiteID | Casino Operations & Locations |
| ID_ExpiryDt | Regulatory & Compliance |
| ID_IssuCountry | Regulatory & Compliance |
| ID_IssuCountryCde | Regulatory & Compliance |
| ID_IssuState | Regulatory & Compliance |
| ID_IssuStateCde | Regulatory & Compliance |
| ID_Num | Regulatory & Compliance |
| ID_PntsFlg | Regulatory & Compliance |
| ID_Type | Regulatory & Compliance |
| Initials | Customer & Loyalty Management |
| InvalidEmailFlg | Customer & Loyalty Management |
| InvalidSMSFlg | Customer & Loyalty Management |
| JnktOperFlg | Customer & Loyalty Management |
| LGA_Name | Customer & Loyalty Management |
| LGA_Name_P | Customer & Loyalty Management |
| LGA_Num | Customer & Loyalty Management |
| LGA_Num_P | Customer & Loyalty Management |
| LGA_Type | Customer & Loyalty Management |
| LGA_TypeDesc | Customer & Loyalty Management |
| LGA_TypeDesc_P | Customer & Loyalty Management |
| LGA_Type_P | Customer & Loyalty Management |
| LastName | Customer & Loyalty Management |
| LatDegrees | Customer & Loyalty Management |
| LatDegrees_P | Customer & Loyalty Management |
| LongDegrees | Customer & Loyalty Management |
| LongDegrees_P | Customer & Loyalty Management |
| LoyaltyProgram | Customer & Loyalty Management |
| MEL_PatronSegID | Customer & Loyalty Management |
| MRMbrFlg | Customer & Loyalty Management |
| MailSts | Customer & Loyalty Management |
| MailStsCde | Customer & Loyalty Management |
| MailTo | Customer & Loyalty Management |
| MailToCde | Customer & Loyalty Management |
| MarketingPty | Casino Operations & Locations |
| MarketingPtyLocNum | Casino Operations & Locations |
| MarketingSiteID | Casino Operations & Locations |
| MbrClsGrp | Customer & Loyalty Management |
| MbrHubAccess | Customer & Loyalty Management |
| MbrshpID | Customer & Loyalty Management |
| MbrshpLvl | Customer & Loyalty Management |
| MbrshpSubTyp | Customer & Loyalty Management |
| MbrshpTyp | Customer & Loyalty Management |
| MelAdminSts | Regulatory & Compliance |
| Mel_AnnlNetLossLmtAmt | Regulatory & Compliance |
| Mel_DailyNetLossLmtAmt | Regulatory & Compliance |
| Mel_DailyTmLmtAmt | Regulatory & Compliance |
| Mel_LegacyPatronNum | Customer & Loyalty Management |
| Mel_LegacyPatronNumChar | Customer & Loyalty Management |
| Mel_MbrCls | Customer & Loyalty Management |
| Mel_PersHostEmpFirstName | Customer & Loyalty Management |
| Mel_PersHostEmpID | Customer & Loyalty Management |
| Mel_PersHostEmpLastName | Customer & Loyalty Management |
| Mel_StopCodes | Regulatory & Compliance |
| MiddleName | Customer & Loyalty Management |
| MigratedFlg | Reference & Time Data |
| MobilePhone | Customer & Loyalty Management |
| NetworkDesc | Customer & Loyalty Management |
| NetworkMbrTyp | Customer & Loyalty Management |
| NetworkName | Customer & Loyalty Management |
| NumAncillaryCards | Customer & Loyalty Management |
| Occupation | Customer & Loyalty Management |
| OccupationCde | Customer & Loyalty Management |
| PASClctdDt | Customer & Loyalty Management |
| PASDelMethod | Customer & Loyalty Management |
| PASOpt | Customer & Loyalty Management |
| PASSignedUpDt | Customer & Loyalty Management |
| PASViewedDt | Customer & Loyalty Management |
| PATRONID | Customer & Loyalty Management |
| PER_PatronSegID | Customer & Loyalty Management |
| PatronName | Customer & Loyalty Management |
| PatronNumber | Customer & Loyalty Management |
| PatronNumberChar | Customer & Loyalty Management |
| PatronSecLvl | Customer & Loyalty Management |
| PerAdminSts | Regulatory & Compliance |
| Per_AnnlNetLossLmtAmt | Regulatory & Compliance |
| Per_DailyNetLossLmtAmt | Regulatory & Compliance |
| Per_DailyTmLmtAmt | Regulatory & Compliance |
| Per_LegacyPatronNum | Customer & Loyalty Management |
| Per_LegacyPatronNumChar | Customer & Loyalty Management |
| Per_MbrCls | Customer & Loyalty Management |
| Per_PersHostEmpFirstName | Customer & Loyalty Management |
| Per_PersHostEmpID | Customer & Loyalty Management |
| Per_PersHostEmpLastName | Customer & Loyalty Management |
| Per_StopCodes | Regulatory & Compliance |
| PhoneFlg | Customer & Loyalty Management |
| Phone_Resp_H | Customer & Loyalty Management |
| Phone_Resp_M | Customer & Loyalty Management |
| Phone_Resp_O | Customer & Loyalty Management |
| Phone_Resp_W | Customer & Loyalty Management |
| Phone_Sts_Cde_H | Customer & Loyalty Management |
| Phone_Sts_Cde_M | Customer & Loyalty Management |
| Phone_Sts_Cde_O | Customer & Loyalty Management |
| Phone_Sts_Cde_W | Customer & Loyalty Management |
| Phone_Sts_Des_H | Customer & Loyalty Management |
| Phone_Sts_Des_M | Customer & Loyalty Management |
| Phone_Sts_Des_O | Customer & Loyalty Management |
| Phone_Sts_Des_W | Customer & Loyalty Management |
| Phone_Valid_Sts_H | Customer & Loyalty Management |
| Phone_Valid_Sts_M | Customer & Loyalty Management |
| Phone_Valid_Sts_O | Customer & Loyalty Management |
| Phone_Valid_Sts_W | Customer & Loyalty Management |
| PlyrRefer | Customer & Loyalty Management |
| PntsBalBand | Customer & Loyalty Management |
| Post_Country | Customer & Loyalty Management |
| Post_CountryCde | Customer & Loyalty Management |
| Post_PostCde | Customer & Loyalty Management |
| Post_State | Customer & Loyalty Management |
| Post_StateCde | Customer & Loyalty Management |
| Post_StreetLine1 | Customer & Loyalty Management |
| Post_StreetLine2 | Customer & Loyalty Management |
| Post_Suburb | Customer & Loyalty Management |
| PrefContactLang | Customer & Loyalty Management |
| PrefContactLangCde | Customer & Loyalty Management |
| PrefNameFlg | Customer & Loyalty Management |
| Pref_FirstName | Customer & Loyalty Management |
| Pref_LastName | Customer & Loyalty Management |
| Pref_MiddleName | Customer & Loyalty Management |
| Pref_Name | Customer & Loyalty Management |
| Pref_Suffix | Customer & Loyalty Management |
| Pref_Title | Customer & Loyalty Management |
| PriPatronCardFlg | Customer & Loyalty Management |
| PriPatronNum | Customer & Loyalty Management |
| PriPrivCardName | Customer & Loyalty Management |
| PrivLockoutFlg | Regulatory & Compliance |
| PrivLockoutLst | Regulatory & Compliance |
| PrivLockoutSrc | Regulatory & Compliance |
| Prom_Material_Ind | Promotions & Marketing |
| ReferredEmpID | Customer & Loyalty Management |
| Res_Country | Customer & Loyalty Management |
| Res_CountryCde | Customer & Loyalty Management |
| Res_PostCde | Customer & Loyalty Management |
| Res_State | Customer & Loyalty Management |
| Res_StateCde | Customer & Loyalty Management |
| Res_StreetLine1 | Customer & Loyalty Management |
| Res_StreetLine2 | Customer & Loyalty Management |
| Res_Suburb | Customer & Loyalty Management |
| Rgn | Customer & Loyalty Management |
| SMSFlg | Customer & Loyalty Management |
| ScdryAccntRsn | Customer & Loyalty Management |
| ScdryPrivCardName | Customer & Loyalty Management |
| SctyCde | Customer & Loyalty Management |
| SignUpChannel | Customer & Loyalty Management |
| SignUpPty | Casino Operations & Locations |
| SignUpPtyLocNum | Casino Operations & Locations |
| SignUpSiteID | Casino Operations & Locations |
| SignupCls | Customer & Loyalty Management |
| SingleNameInd | Customer & Loyalty Management |
| SourceCde | Reference & Time Data |
| Spouse | Customer & Loyalty Management |
| Suffix | Customer & Loyalty Management |
| Syd_AdminSts | Regulatory & Compliance |
| Syd_DailyNetLossLmtAmt | Regulatory & Compliance |
| Syd_DailyTmLmtAmt | Regulatory & Compliance |
| Syd_HighPrtyCmt | Regulatory & Compliance |
| Syd_PatronSegID | Customer & Loyalty Management |
| Syd_StopCodes | Regulatory & Compliance |
| T200Flg | Customer & Loyalty Management |
| Title | Customer & Loyalty Management |
| Undesirable_Wanted_Ind | Regulatory & Compliance |
| UnifiedDt | Reference & Time Data |
| UnifiedDtTm | Reference & Time Data |
| UnifiedFlg | Customer & Loyalty Management |
| VIC_Country_Metro_Ind | Customer & Loyalty Management |
| VIP_ClubLvl | Customer & Loyalty Management |
| VIP_ClubTagNum | Customer & Loyalty Management |
| WorkPhone | Customer & Loyalty Management |
| YourPlayFlg | Customer & Loyalty Management |

### D_PRODUCT

| Field | Domain |
|-------|--------|
| AltGamingActvyCde | Gaming Products & Assets |
| EGM_DENOM | Gaming Products & Assets |
| EGM_GAMECODE | Gaming Products & Assets |
| ETLJobDtlID | Reference & Time Data |
| GAMENAME | Gaming Products & Assets |
| GAMINGACTIVITYCODE | Gaming Products & Assets |
| GAMINGPRODTYP | Gaming Products & Assets |
| PRODUCTID | Gaming Products & Assets |
| SctyCde | Gaming Products & Assets |
| SiteID | Casino Operations & Locations |

### D_PRODUCTDET

| Field | Domain |
|-------|--------|
| AltGamingActvyCde | Gaming Products & Assets |
| AltSubGameCde | Gaming Products & Assets |
| AltSubGameName | Gaming Products & Assets |
| EGMLines | Gaming Products & Assets |
| EGM_DENOM | Gaming Products & Assets |
| EGM_GAMECODE | Gaming Products & Assets |
| ETLJobDtlID | Reference & Time Data |
| EdgeTheo | Gaming Products & Assets |
| GAMENAME | Gaming Products & Assets |
| GAMINGACTIVITYCODE | Gaming Products & Assets |
| GAMINGPRODTYP | Gaming Products & Assets |
| GameTyp | Gaming Products & Assets |
| JACKPOTFLG | Gaming Products & Assets |
| PRODUCTDETID | Gaming Products & Assets |
| RwrdLvl | Gaming Products & Assets |
| SUBGAMECODE | Gaming Products & Assets |
| SUBGAMENAME | Gaming Products & Assets |
| SctyCde | Reference & Time Data |
| SiteID | Casino Operations & Locations |
| TBLLVL | Gaming Products & Assets |
| TBLMINBET | Gaming Products & Assets |
| TblMaxBet | Gaming Products & Assets |

### D_Plyr_Prog

| Field | Domain |
|-------|--------|
| CompRolloverAmt | Customer & Loyalty Management |
| CompRolloverExpDt | Customer & Loyalty Management |
| CumulativeCompValEarnedToDt | Customer & Loyalty Management |
| CumulativeCompValUsedToDt | Customer & Loyalty Management |
| DaysProgOpnToDt | Customer & Loyalty Management |
| ETLJobDtlID | Reference & Time Data |
| OpnCompRolloverAmt | Customer & Loyalty Management |
| PPPAFlg | Customer & Loyalty Management |
| PatronID | Customer & Loyalty Management |
| PrgPlyrSts | Customer & Loyalty Management |
| ProgCatg | Customer & Loyalty Management |
| ProgCde | Customer & Loyalty Management |
| ProgCntry | Customer & Loyalty Management |
| ProgCntryName | Customer & Loyalty Management |
| ProgCommRate | Customer & Loyalty Management |
| ProgCommTOBasis | Customer & Loyalty Management |
| ProgCompAllowRate | Customer & Loyalty Management |
| ProgCompAllowTOBasis | Customer & Loyalty Management |
| ProgCrcyTyp | Customer & Loyalty Management |
| ProgEarlyPayCommRate | Customer & Loyalty Management |
| ProgEarlyPayDiscOnLossPct | Customer & Loyalty Management |
| ProgEndDt | Customer & Loyalty Management |
| ProgGrp | Customer & Loyalty Management |
| ProgID | Customer & Loyalty Management |
| ProgLastUpdtDt | Reference & Time Data |
| ProgName | Customer & Loyalty Management |
| ProgNotes | Customer & Loyalty Management |
| ProgNum | Customer & Loyalty Management |
| ProgOfcCde | Casino Operations & Locations |
| ProgOfcName | Casino Operations & Locations |
| ProgPayTypCde | Customer & Loyalty Management |
| ProgPayTypDesc | Customer & Loyalty Management |
| ProgRbtOnLossPct | Customer & Loyalty Management |
| ProgRbtTypCde | Customer & Loyalty Management |
| ProgRbtTypDesc | Customer & Loyalty Management |
| ProgRgn | Customer & Loyalty Management |
| ProgStartDt | Customer & Loyalty Management |
| ProgState | Customer & Loyalty Management |
| ProgStateName | Customer & Loyalty Management |
| ProgSts | Customer & Loyalty Management |
| ProgTaxRate | Customer & Loyalty Management |
| ProgTypCde | Customer & Loyalty Management |
| ProgTypDesc | Customer & Loyalty Management |
| ProgTypValCls | Customer & Loyalty Management |
| PtyLocName | Casino Operations & Locations |
| PtyLocNum | Casino Operations & Locations |
| SctyCde | Reference & Time Data |
| Segment | Customer & Loyalty Management |
| SiteID | Casino Operations & Locations |

### D_Site

| Field | Domain |
|-------|--------|
| SctyCde | Casino Operations & Locations |
| SiteGrpName | Casino Operations & Locations |
| SiteID | Casino Operations & Locations |
| SiteName | Casino Operations & Locations |
| SiteNum | Casino Operations & Locations |

### D_Status_Code

| Field | Domain |
|-------|--------|
| StsCde | Reference & Time Data |
| StsDesc | Reference & Time Data |
| StsID | Reference & Time Data |
| StsTyp | Reference & Time Data |

### D_TRANSTYPE

| Field | Domain |
|-------|--------|
| ETLJobDtlID | Reference & Time Data |
| LegacyTransCde | Reference & Time Data |
| LegacyTransDesc | Reference & Time Data |
| SctyCde | Reference & Time Data |
| SiteID | Casino Operations & Locations |
| TRANSTYPECODE | Gaming Activity & Performance |
| TRANSTYPEDESC | Gaming Activity & Performance |
| TRANSTYPEID | Gaming Activity & Performance |
| TransGrp | Gaming Activity & Performance |

### D_jackpot_product_type

| Field | Domain |
|-------|--------|
| ETLJobDtlID | Reference & Time Data |
| JkptProdTyp | Gaming Products & Assets |
| JkptProdTypID | Gaming Products & Assets |
| JkptProdTypOrder | Gaming Products & Assets |
| SctyCde | Gaming Products & Assets |
| SiteID | Casino Operations & Locations |

### F_GAMINGRATING

| Field | Domain |
|-------|--------|
| ACTUALWIN | Gaming Activity & Performance |
| AGEID | Customer & Loyalty Management |
| AVGBET | Gaming Activity & Performance |
| BONUS | Gaming Activity & Performance |
| BUYIN | Gaming Activity & Performance |
| CASINOCASHEARNED | Gaming Activity & Performance |
| CASINOLOCATIONID | Casino Operations & Locations |
| CASINOLOCDETID | Casino Operations & Locations |
| CashlessIn | Gaming Activity & Performance |
| DEALERID | Casino Operations & Locations |
| DeptID | Casino Operations & Locations |
| EGMAdjustedTHEOWIN | Gaming Activity & Performance |
| EGMStroke | Gaming Activity & Performance |
| EGM_PNTSEARNED | Customer & Loyalty Management |
| ETLJobDtlID | Reference & Time Data |
| GAMINGMACHINEID | Gaming Products & Assets |
| GameWins | Gaming Activity & Performance |
| GrossRev | Gaming Activity & Performance |
| HOURSPLAYED | Gaming Activity & Performance |
| JACKPOT | Gaming Activity & Performance |
| JkptProdTypID | Gaming Products & Assets |
| JnktRatingFlg | Gaming Activity & Performance |
| LEGACYPATRONID | Customer & Loyalty Management |
| LegacyAuditStsCde | Regulatory & Compliance |
| LicID | Regulatory & Compliance |
| LimitHitDtandTm | Gaming Activity & Performance |
| LimitHitHrID | Gaming Activity & Performance |
| NetRev | Gaming Activity & Performance |
| NumBets | Gaming Activity & Performance |
| PATRONID | Customer & Loyalty Management |
| PNTSEARNED | Customer & Loyalty Management |
| PRODUCTDETID | Gaming Products & Assets |
| PRODUCTID | Gaming Products & Assets |
| PROGNUM | Customer & Loyalty Management |
| PatronAncillaryCardID | Customer & Loyalty Management |
| PntsEarnedFB | Customer & Loyalty Management |
| PntsEarnedHotel | Customer & Loyalty Management |
| PntsEarnedOther | Customer & Loyalty Management |
| PntsEarnedRetl | Customer & Loyalty Management |
| PntsEarnedRetlTency | Customer & Loyalty Management |
| PointEarningRatio | Customer & Loyalty Management |
| ProgCompValEarned | Customer & Loyalty Management |
| ProgID | Customer & Loyalty Management |
| ProgOfcID | Customer & Loyalty Management |
| RATINGENDDTTM | Gaming Activity & Performance |
| RATINGHOURID | Gaming Activity & Performance |
| RATINGID | Gaming Activity & Performance |
| RATINGSTARTDTTM | Gaming Activity & Performance |
| RatingEndHrID | Gaming Activity & Performance |
| RatingType | Gaming Activity & Performance |
| SECONDSPLAYED | Gaming Activity & Performance |
| SUPERID | Casino Operations & Locations |
| SctyCde | Regulatory & Compliance |
| SiteID | Casino Operations & Locations |
| StsID | Reference & Time Data |
| TBLPNTSEARNED | Customer & Loyalty Management |
| THEOWIN | Gaming Activity & Performance |
| TRANSTYPEID | Gaming Activity & Performance |
| TURNOVER | Gaming Activity & Performance |
| TblCheqIn | Gaming Activity & Performance |
| TblChipsIn | Gaming Activity & Performance |
| TblCshIn | Gaming Activity & Performance |
| Terminallocationdetid | Casino Operations & Locations |
| VALIDCODE | Reference & Time Data |
| VIP_PNTSEARNED | Customer & Loyalty Management |

### F_Promotion_Transaction

| Field | Domain |
|-------|--------|
| ActndResourceID | Gaming Products & Assets |
| AuthEmpLicID | Casino Operations & Locations |
| BillToDeptID | Casino Operations & Locations |
| Budg | Promotions & Marketing |
| CompType | Promotions & Marketing |
| CompletelyRdmdFlg | Promotions & Marketing |
| Cost | Promotions & Marketing |
| ETLJobDtlID | Reference & Time Data |
| FaceValDlrAmt | Promotions & Marketing |
| GeneratedbySysCde | Reference & Time Data |
| GenericAuditStsCde | Reference & Time Data |
| IntTrsfrDlrAmt | Promotions & Marketing |
| LegacyAuditStsCde | Reference & Time Data |
| LegacyPatronID | Customer & Loyalty Management |
| LegacyPromoID | Promotions & Marketing |
| LegacyPromoTyp | Promotions & Marketing |
| NumCredits | Gaming Activity & Performance |
| NumPnts | Customer & Loyalty Management |
| PartRdmdFlg | Promotions & Marketing |
| PatronID | Customer & Loyalty Management |
| PeakRedemptionFlg | Promotions & Marketing |
| ProgID | Customer & Loyalty Management |
| ProgNum | Customer & Loyalty Management |
| PromoCmtID | Reference & Time Data |
| PromoDeptID | Promotions & Marketing |
| PromoID | Promotions & Marketing |
| PromoTransDtTm | Promotions & Marketing |
| PromoTransHrID | Reference & Time Data |
| PromoTransLocID | Casino Operations & Locations |
| Qty | Promotions & Marketing |
| SctyCde | Regulatory & Compliance |
| SiteID | Casino Operations & Locations |
| TransCmtFlg | Reference & Time Data |
| UnitVal | Promotions & Marketing |
| ValidCde | Reference & Time Data |

### sybaseadmin.D_CASINOLOCATIONDET

| Field | Domain |
|-------|--------|
| BusOwnID | Casino Operations & Locations |
| BusOwnName | Casino Operations & Locations |
| BusOwnSctyCde | Casino Operations & Locations |
| CASINOLOC | Casino Operations & Locations |
| CASINOLOCDETID | Casino Operations & Locations |
| CasinoLocDesc | Casino Operations & Locations |
| EGMAreaName | Casino Operations & Locations |
| EGMBankName | Casino Operations & Locations |
| EGMZoneCde | Casino Operations & Locations |
| EGMZoneDesc | Casino Operations & Locations |
| EGM_AREA | Casino Operations & Locations |
| EGM_BANK | Casino Operations & Locations |
| EGM_MACHINE | Casino Operations & Locations |
| ETLJobDtlID | Reference & Time Data |
| GAMINGAREA | Casino Operations & Locations |
| GAMINGTABLENUM | Casino Operations & Locations |
| GamingAreaName | Casino Operations & Locations |
| GamingAreaSeg | Casino Operations & Locations |
| GamingAreaSegName | Casino Operations & Locations |
| GamingAreaStrm | Casino Operations & Locations |
| GamingAreaSubSeg | Casino Operations & Locations |
| LOCTYPCODE | Casino Operations & Locations |
| LegacyDeptNum | Casino Operations & Locations |
| LocTypName | Casino Operations & Locations |
| MicrosRevCent | Casino Operations & Locations |
| MicrosRevCentDesc | Casino Operations & Locations |
| NumSGStns | Casino Operations & Locations |
| OperaRevCent | Casino Operations & Locations |
| OutletArea | Casino Operations & Locations |
| OutletLvl | Casino Operations & Locations |
| OutletStyle | Casino Operations & Locations |
| OutletTyp | Casino Operations & Locations |
| PITNUM | Casino Operations & Locations |
| PTYLOCNAME | Casino Operations & Locations |
| PTYLOCNUM | Casino Operations & Locations |
| PagingZone | Casino Operations & Locations |
| SctyCde | Casino Operations & Locations |
| SiteID | Casino Operations & Locations |
| TBLAREA | Casino Operations & Locations |
| TblNum | Casino Operations & Locations |

### sybaseadmin.D_TerminalLocationDet

| Field | Domain |
|-------|--------|
| CASINOLOC | Casino Operations & Locations |
| CASINOLOCDETID | Casino Operations & Locations |
| CasinoLocDesc | Casino Operations & Locations |
| ETLJobDtlID | Reference & Time Data |
| GAMINGAREA | Casino Operations & Locations |
| GamingAreaName | Casino Operations & Locations |
| GamingAreaSeg | Casino Operations & Locations |
| GamingAreaStrm | Casino Operations & Locations |
| GamingAreaSubSeg | Casino Operations & Locations |
| GamingTableNum | Casino Operations & Locations |
| NumSGStns | Casino Operations & Locations |
| PITNUM | Casino Operations & Locations |
| PagingZone | Casino Operations & Locations |
| SctyCde | Casino Operations & Locations |
| SiteID | Casino Operations & Locations |
| TBLAREA | Casino Operations & Locations |
| TerminalLoc | Casino Operations & Locations |
| TerminalLocationDetID | Casino Operations & Locations |
| TerminalNum | Casino Operations & Locations |

