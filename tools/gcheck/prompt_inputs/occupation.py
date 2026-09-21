"""Group 1: O*NET occupation and task-pick pairing against the prompt (M1-M3).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from ..common import load_metadata
from ..core import check, emit, recommend, REPORT, OPTIONS


# M2: O*NET task picks whose duty has no signal in the prompt. Key is a regex
# matching the picked task line; value is (level, label, regex of prompt signals).
# ERROR rows are the duty-specific picks the platform's Skills prompt relevance
# check has already rejected or would obviously reject; the rest are softer signals.
ONET_TASK_FIT = [
    # --- 11-3061.00 Purchasing Managers ---
    (r"develop and implement purchasing and contract management instructions", "ERROR",
     "writing, revising or rolling out a purchasing policy or procedure",
     r"(?:write|writ(?:e|ing)|draft|revis|rewrit|new|roll(?:ing)? out|put in place|implement)\w* (?:a |the |our )?(?:policy|procedure|ground rules|instructions?)|policy (?:change|rewrite|revision)"),
    # Added 2026-08-31 (radke-price-protection round 2 of the Skills prompt relevance
    # check): 13-1022's sixteen tasks contain nothing about maintaining purchase records,
    # verifying claims or preparing cost reports, so a claims/records prompt CANNOT field
    # three strong picks there and the fix is the occupation, not another pick (the
    # routing table's row for vendor program administration; pavelka cleared the same
    # check under 11-3061). Rows cover the picks the portfolio uses.
    (r"review purchase order claims and contracts for conformance", "ERROR",
     "verifying claims or contracts against policy or program terms",
     r"claim|conformance|program|policy|terms|rules|agreement|qualif"),
    (r"resolve vendor or contractor grievances and claims against suppliers", "ERROR",
     "a claim or grievance against a supplier",
     r"claim|credit|protection|dispute|grievance|owes?|filing|file|recover"),
    (r"maintain records of goods ordered and received", "ERROR",
     "purchase and receipt records",
     r"receipt|register|record|purchase order|open (?:po|order)|received|cage|count"),
    (r"prepare reports regarding market conditions and merchandise costs", "ERROR",
     "reporting on market conditions or merchandise costs",
     r"cost|price|column|market|copper|report|briefing|page (?:she|he|they|lavina)|workbook"),
    (r"represent companies in negotiating contracts and formulating policies", "ERROR",
     "negotiating contracts or formulating supplier policies",
     r"negotiat|contract|agreement|terms|policy|renewal|position"),
    # --- 13-1022.00 Wholesale and Retail Buyers, Except Farm Products ---
    # Added 2026-08-31 (radke-price-protection, Skills prompt relevance FAIL): the checker
    # retained all four skills but failed the section because two of three task picks were
    # "weakly related or unrelated" - "Authorize payment of invoices or return of
    # merchandise" with no payment/RTV work requested, and "Collaborate with vendors to
    # obtain or develop desired products" against a price-protection filing that develops
    # nothing. Each pick is read against the prompt's actual requested work (the same rule
    # M2 already applies to 11-3071), so every verbatim 13-1022 string the portfolio has
    # ever picked gets a signal here. Signals are generous on purpose: a false positive
    # costs a pre-submission reword, a false negative costs a platform cycle.
    (r"authorize payment of invoices or return of merchandise", "ERROR",
     "authorizing invoice payment or returning merchandise",
     r"authoriz|approve|pay(?:ing|ment)? (?:the |an )?invoice|return (?:it|the|them)|"
     r"RTV|send (?:it|them) back|chargeback|short[- ]?pay"),
    (r"collaborate with vendors to obtain or develop desired products", "ERROR",
     "working with a vendor to source or develop a product",
     r"develop|source|new (?:product|item|line|size)|special[- ]order|"
     r"work(?:ing)? with (?:the )?(?:vendor|supplier|mill|factory)|have them (?:make|build|run)"),
    (r"inspect merchandise or products to determine quality, value, or yield", "ERROR",
     "inspecting merchandise for quality, value or yield",
     r"inspect|condition|sealed|cut|damag|quality|grade|yield|count(?:ed)? the|recount"),
    (r"monitor and analyze sales records, trends, or economic conditions", "ERROR",
     "analyzing sales, movement or inventory records",
     r"sales|invoice lines|movement|history|records?|register|trend|usage|"
     r"item file|cage count|receipts|demand|needed inventory"),
    (r"negotiate prices, discount terms, or transportation arrangements", "ERROR",
     "negotiating prices, discount terms or freight with a supplier",
     r"negotiat|price|discount|freight|prepaid|terms|credit|program|"
     r"get back|press|ask(?:s|ing)?"),
    (r"examine, select, order, or purchase merchandise consistent with", "ERROR",
     "selecting, ordering or purchasing merchandise",
     r"order|buy|purchas|stock(?:ing)?|reorder|assortment|carry|quantit"),
    (r"buy merchandise or commodities for resale", "ERROR",
     "buying merchandise for resale",
     r"buy|order|purchas|program buy|early[- ]buy|book(?:ing)? the (?:order|buy)"),
    (r"recommend mark-up rates, mark-down rates, or merchandise selling prices", "ERROR",
     "setting mark-up, mark-down or selling prices",
     r"mark[- ]?up|mark[- ]?down|sell(?:ing)? price|resale|margin|price to the customer"),
    (r"obtain information about customer needs or preferences by conferring", "ERROR",
     "conferring with sales or purchasing personnel about customer needs",
     r"customer|counter|branch manager|sales(?:men|man| desk| floor| people)?|"
     r"confer|what (?:the branches|they) (?:need|want|are asking)"),
    # --- 11-3071.00 Transportation, Storage, and Distribution Managers ---
    (r"warehouse safety and security programs", "ERROR", "warehouse safety or security programs",
     r"safety|security|hazard|osha|lock ?out|fire\b|guard"),
    (r"interview, select, and train|supervise the activities of workers|"
     r"work of subordinate staff", "ERROR", "supervising or staffing warehouse personnel",
     r"\bsupervis|\bour (?:men|people|crew)\b|assign the work|\bshift\b|headcount|"
     r"hire|\btrain(?:ing|ed)?\b|payroll"),
    (r"prepare and manage departmental budgets|analyze expenditures and other financial",
     "ERROR", "departmental budgeting", r"budget|expense plan|profit plan|spending plan"),
    (r"monitor product import or export|tariff and customs", "ERROR",
     "import, export or customs compliance", r"import|export|customs|\bduty\b|broker|entry summary"),
    (r"negotiate with carriers, warehouse operators", "ERROR",
     "negotiating rates with carriers, warehousemen or insurers",
     r"negotiat|preferential|\brate\b|tariff|quote a rate|press (?:them|him|her)"),
    (r"direct the use of drones", "ERROR", "drones or autonomous vehicles", r"drone|autonomous"),
    (r"energy saving changes to transportation", "ERROR", "energy or emissions reduction",
     r"energy|emission|idling|fuel|carbon"),
    (r"salvaging products or materials", "ERROR",
     "emergency handling, storage or salvage procedure",
     r"salvage|segregat|emergency|storm|damage|disposal|haul|scrap|procedure|"
     r"policy|bulletin|condition"),
    (r"monitor inventory levels of products or materials in warehouses", "ERROR",
     "the warehouse inventory position",
     r"inventory|\bstock\b|on hand|\bbins?\b|warehouse|location status|aisle|\brack\b|count"),
    (r"resolve problems concerning transportation, logistics systems", "ERROR",
     "a logistics or customer service problem",
     r"customer|\border\b|promise|late\b|short|cannot (?:make|ship|cover)|backlog|counter"),
    (r"collaborate with other departments to integrate logistics", "ERROR",
     "work across sales, order management or accounting",
     r"customer|\border\b|counter|account|controller|sales|billing|invoice|purchasing"),
    (r"examine invoices and shipping manifests", "ERROR", "invoice and manifest verification",
     r"invoice|manifest|packing list|bill of lading|receipt|receiving"),
    # --- 11-3061.00 Purchasing Managers ---
    (r"resolve vendor or contractor grievances and claims", "ERROR",
     "resolving a vendor grievance or a claim against a supplier",
     r"claim|grievance|dispute|credit|deposit|owed?\b|owes?\b|shortage|refund|recover"),
    (r"represent companies in negotiating contracts", "ERROR",
     "negotiating a supplier contract or its terms",
     r"contract|agreement|\bterms\b|negotiat|sign(?:ing|ed)?\b|commitment|offer"),
    (r"review purchase order claims and contracts for conformance", "ERROR",
     "reviewing purchase order claims or contracts against company policy",
     r"purchase order|open (?:po|order)|\bpo\b|policy|ground rules|conformance|"
     r"memo|her rules"),
    (r"develop cost reduction strategies|control purchasing department budgets",
     "ERROR", "purchasing budgets or cost reduction programs",
     r"budget|cost reduction|savings plan|spend(?:ing)? (?:plan|target)"),
    # packaging-consolidation AutoEval 2026-09-05: "requiring board approval" is part of the pick
    # and a prompt with bids but no board was called an added context; the pick needs a board
    (r"prepare bid awards", "ERROR", "a bid award that goes to a board",
     r"\bboard\b|directors|trustees|council|commission(?:ers)?\b"),
    (r"approve specifications for issuing and awarding bids",
     "ERROR", "issuing or awarding bids", r"\bbid\b|award|rfq|request for quot"),
    (r"interview and hire staff|direct and coordinate activities of personnel",
     "ERROR", "staffing or supervising purchasing personnel",
     r"hire|staff|supervis|\btrain(?:ing|ed)?\b|headcount"),
    (r"arrange for disposal of surplus", "ERROR", "surplus disposal",
     r"surplus|disposal|scrap|obsolete|liquidat"),
    (r"locate vendors of materials", "ERROR", "sourcing new vendors",
     r"new (?:vendor|supplier|source)|locate|alternate (?:vendor|supplier|source)|"
     r"second source|qualif"),
    (r"analyze market and delivery systems", "ERROR",
     "market or material availability analysis",
     r"availability|market|lead ?time|allocation|shortage|supply"),
    # --- 13-1022.00 Wholesale and Retail Buyers, Except Farm Products ---
    (r"negotiate prices, discount terms", "ERROR", "supplier negotiation",
     r"negotiat|discount|concession|counter ?offer|rebate|terms letter|"
     r"press (?:them|him|her)|hold (?:the )?(?:price|line) on|ask(?:ed|ing)? for a better|"
     r"freight|prepaid|zone rate|carrier|transportation|ship point|delivered pric"),
    (r"consult with store or merchandise managers about budgets", "ERROR",
     "budget or assortment consultation",
     r"budget|assortment|open to buy|what to stock|stocking (?:list|decision)|"
     r"line review|add(?:ing)? the line|drop(?:ping)? the line|carry the line"),
    (r"monitor and analyze sales records, trends", "ERROR", "trend or demand forecasting",
     r"trend|forecast|seasonal|anticipat|run rate|usage|demand|movement|"
     r"turns?\b|history|historical|what (?:we|they) (?:sell|move)|"
     r"unit sales|sales (?:record|histor|by|volume)"),
    (r"recommend mark-?up rates", "ERROR", "pricing or margin setting",
     r"mark ?up|mark ?down|sell(?:ing)? price|price list|margin|price sheet|multiplier"),
    (r"conduct sales meetings", "ERROR", "introducing new merchandise",
     r"sales meeting|introduc|new line|new product|roll ?out|launch"),
    (r"train or supervise", "ERROR", "training or supervision",
     r"train|supervis|coach|staffing|headcount"),
    (r"advertis|price tags|competitors' sales activities", "ERROR", "advertising or retail pricing support",
     r"advertis|promo|flyer|price tag|circular|competitor"),
    (r"\bgreen\b|environmental aspects|energy-efficient", "ERROR", "green or environmental sourcing",
     r"green\b|environmental|carbon|energy|sustainab|recycl"),
    (r"obtain information about customer needs", "ERROR", "customer needs gathered from sales personnel",
     r"customer|account|branch manager|outside sales|salesman|sales rep|counter"),
    (r"authorize payment of invoices or return", "ERROR", "invoice payment or merchandise return",
     r"invoice|return|credit|claim|send(?:ing)? back|charge ?back|debit"),
    (r"inspect merchandise or products", "ERROR", "inspecting stock for quality or value",
     r"inspect|quality|defect|date code|lot|good to sell|condition|scrap|damage"),
    (r"collaborate with vendors", "ERROR", "working the vendor directly",
     r"vendor|supplier|factory|mill\b|manufacturer|rep\b|district manager|"
     r"bulletin|their form|ships? again|rep_email|surplus house|quotation|allocation"),
    (r"buy merchandise or commodities for resale", "ERROR", "buying for resale",
     r"buy\b|bought|purchase|\border\b|stock up|cover the|substitut|replac|"
     r"keep selling|resale|resell|keep .{0,20}(?:bins?|shelves|shelf) "),
    (r"examine, select, order, or purchase merchandise", "ERROR", "specification-driven selection",
     r"spec|rated|substitut|equivalent|cross|qualif|quality|quantity|good to sell|"
     r"stocked item|stocking|replenish|order point|order quantit|settings"),
    # --- 11-2022.00 Sales Managers (commission-review-q2 AutoEval, 2026-09-05: the customer
    # complaints pick FAILed the whole section on a prompt whose disputes were the reps' own
    # commission disputes, and the direct-and-coordinate-sales pick was called only indirectly
    # related to a commission audit) ---
    (r"resolve customer complaints regarding sales", "ERROR",
     "a customer's complaint about sales or service",
     r"customer'?s? (?:complain|dispute|backcharge|claim)|complain\w* (?:from|by) (?:a |the )?customer"
     r"|customers? (?:are |have |who )?(?:complain|disput|call(?:ed|ing)? (?:in|about|the counter))|backcharge"),
    (r"direct and coordinate activities involving sales of", "ERROR",
     "directing the selling activity itself",
     r"sales (?:call|team|territor|quota|campaign|meeting|coverage)|territor|selling|sales rep\w* (?:call|cover|visit)|call plan"),
    # second round the same day: the staffing pick was called "clearly unrelated" to a commission
    # audit even with commission words everywhere, so pay words do not count as a signal for it
    (r"plan and direct staffing, training, and performance evaluations", "ERROR",
     "staffing, training or performance evaluation of sales staff",
     r"staffing|hire|hiring|training|performance (?:review|evaluation|appraisal)|evaluat(?:e|ing) (?:the |our )?(?:reps?|staff|team)|coach"),
    (r"establish and monitor staff'?s sales goals", "ERROR", "sales goals or quotas",
     r"quota|goal|target|bonus|accelerator"),
    # --- 43-5071.00 Shipping, Receiving, and Inventory Clerks ---
    # Added 2026-09-17 (detention-claim-audit, draft 53, Skills prompt relevance FAIL): the
    # checker retained three picks on a detention claim audit and failed the section on the
    # fourth, "Contact carrier representatives to make arrangements or to issue instructions
    # for shipping and delivery of materials", because auditing a carrier's claim is not
    # arranging its delivery; setting appointments is not a signal either (the prompt said so
    # and the pick still failed). Its steer: picks about auditing records, calculating
    # charges, reconciling discrepancies and preparing accounting or operational reports.
    # Rows cover the picks the portfolio uses.
    (r"contact carrier representatives to make arrangements", "ERROR",
     "arranging a shipment with a carrier or issuing it shipping instructions",
     r"arrang\w* (?:a |the |for |our )?(?:pickup|pick-up|pick up|deliver|shipment|shipping|carrier|truck|collection)"
     r"|book\w* (?:a |the |our )?(?:truck|carrier|pickup|load)"
     r"|schedul\w* (?:a |the |each |our )?(?:pickup|carrier|truck|delivery|load)"
     r"|(?:instruct|tell|notify|advise|call)\w* (?:the |each |every |our )?carriers?\b"
     r"|(?:routing|shipping|delivery|pickup) instructions|tender\w* (?:the |a |each )?(?:load|shipment)"
     r"|dispatch|set up (?:a |the )?(?:pickup|delivery)"),
    (r"compute amounts, such as space available, shipping, storage, or demurrage", "ERROR",
     "computing a shipping, storage or demurrage type charge",
     r"demurrage|detention|accessorial|storage charge|charge|rate|fee|amount|owe|invoice|bill"),
    (r"record shipment data, such as weight, charges", "ERROR",
     "recording shipment charges, damages or discrepancies for accounting or reporting",
     r"record|log|charge|discrepanc|damage|shortage|accounting|report|workbook|register"),
    (r"confer or correspond with establishment representatives to rectify problems", "ERROR",
     "correspondence with a carrier or supplier over a damage, shortage or non-conformance",
     r"correspond|email|letter|written in|wrote|write back|reply|dispute|shortage|damage|nonconform|rectif|complain"),
]


# M3: the "Occupation prompt relevance" check reads the prompt's requested work, not
# the practitioner profile. Under 13-1022 a prompt whose ask reads as another domain's
# job fails even when every duty in it is genuinely merchandise work underneath
# (frankfort-storm-claim, 2026-08-21: "preparing a property-loss claim workbook ...
# those duties are only a limited part of the requested work").
OCCUPATION_FRAMES = [
    ("insurance claim preparation",
     r"\bclaim(?:s|ed|ing)?\b|\badjuster\b|\bexaminer\b|proof of loss|\bdeductible\b|"
     r"\bcoverage\b|\bsublimit\b|\binsur(?:er|ed|ance)\b|\bunderwrit|\bendorsement\b|"
     r"\bpolicy limit\b|\bloss schedule\b"),
    ("litigation support",
     r"\bdeposition\b|\bsubpoena\b|\bplaintiff\b|\bdefendant\b|\boutside counsel\b|"
     r"\bdiscovery request\b|\blitigation\b"),
    ("an audit engagement",
     r"\bauditor\b|\bworkpaper|\bmateriality\b|\bengagement letter\b|\binternal control"),
    # draft 32 pavelka, 2026-08-25: 13-1022 FAILed on a vendor-bankruptcy exposure
    # workup — "reconciling accounts, credits, deposits, claims, bankruptcy exposure,
    # agreement economics, and covenant reporting ... financial analysis and reporting
    # rather than buying merchandise". The vendor-claims/contract-terms version of this
    # work lives on 11-3061.00 Purchasing Managers ("resolve vendor or contractor
    # grievances and claims against suppliers"; "represent companies in negotiating
    # contracts and formulating policies with suppliers"), also Wholesale Trade.
    ("a creditor's bankruptcy exposure and covenant workup",
     r"\bbankrupt|\bchapter (?:7|11)\b|\bpetition(?:\s+date)?\b|\bcreditor|"
     r"\brestructuring\b|\bcovenant|\bdebtor\b|\btrustee\b|\bproof of claim\b|"
     r"\bpre-?petition|\bpost-?petition\b|\bsetoff\b|\bdue in full\b"),
]


MERCHANDISE_SIGNAL = (
    r"\bstock\b|\bbins?\b|\bitem\b|\bmerchandise\b|\bsupplier\b|\bvendor\b|\bbuy\b|"
    r"\bbought\b|\bpurchas|\border\b|\borders\b|mark ?down|mark ?up|\bsell\b|\bsold\b|"
    r"\bprice|\bcost\b|\bpack\b|\btransfer|\bbranch\b|on hand|\busage\b|\bmovement\b|"
    r"\breplenish|\bfreight\b|\blands?\b|\bship|\bcounter\b|\bcustomers?\b|\bstore\b"
)


# A deliverable named for the other domain is the loudest signal the check reads.
FRAME_FILENAME = r"claim|insurance|policy|lawsuit|litigation|audit|settlement_letter"


def _check_occupation_frame(ptext):
    """M3 — under 13-1022, is the prompt's requested work framed as merchandise work?"""
    merch = len(re.findall(MERCHANDISE_SIGNAL, ptext, re.I))
    for label, pat in OCCUPATION_FRAMES:
        frame = len(re.findall(pat, ptext, re.I))
        if frame and frame >= merch * 0.30:
            emit("ERROR", f"[M3] occupation 13-1022 with a prompt that reads as {label} "
                         f"({frame} frame terms against {merch} merchandise terms) — the "
                         "platform's Occupation prompt relevance check judges the work the "
                         "prompt asks for and FAILed frankfort-storm-claim on this "
                         "(2026-08-21). Reframe the ask around the merchandise work the "
                         "deliverable carries and let the other domain enter as the rules "
                         "the values are written on — and if the frame IS the work "
                         "(a warehouse loss, salvage, storage), move the occupation to "
                         "11-3071.00 Transportation, Storage, and Distribution Managers, "
                         "also Wholesale Trade, which carries salvaging materials, "
                         "warehouse inventory levels and insurance company "
                         "representatives in its own task list (frankfort passed there "
                         "with the prompt unchanged); when the frame is vendor claims, "
                         "credits and deposits or a supplier agreement decision, move to "
                         "11-3061.00 Purchasing Managers instead (resolve vendor "
                         "grievances and claims against suppliers; negotiate contracts "
                         "with suppliers — draft 32 pavelka, 2026-08-25)")
    named = re.search(r"named\s+(?:exactly\s+)?([\w.\-]+\.(?:xlsx|docx|csv|pptx))", ptext, re.I)
    if named and re.search(FRAME_FILENAME, named.group(1), re.I):
        emit("ERROR", f"[M3] the deliverable named in the prompt, {named.group(1)}, is named for "
                     "another domain's work product under a buy-side occupation — the "
                     "Occupation prompt relevance check reads the file name too; name the "
                     "deliverable for the merchandise work it carries")


@check(codes=['M1', 'M2', 'M3'], rules=['PRE-OCC'], needs=['metadata', 'prompt'], params=['folder'])
def check_metadata(folder):
    """The O*NET occupation and every task pick match the work the prompt actually requests.

    Codes:
      M1  occupation 13-1022 (buy-side) is never paired with a customer-bid prompt
      M2  every O*NET task pick has a signal of its duty in the prompt
      M3  under 13-1022 the prompt's requested work, and its deliverable's name, read as merchandise work rather than another domain's
    Since: M1 task 08; M2 2026-08-20 (task 13); M3 2026-08-21 (frankfort-storm-claim).
    Source: the platform's O*NET compliance, Skills prompt relevance and Occupation prompt relevance checks.
    """
    meta, prompt = load_metadata(folder), folder / "prompt.md"
    if not (meta and prompt.exists()):
        return
    ptext = prompt.read_text(encoding="utf-8")
    # a Refinery fetch can return no occupation at all (the form hides O*NET); a None code
    # crashed the whole gate on skylark-brookstone-proposal (2026-09-10)
    code = (meta.get("onet_occupation") or {}).get("code") or ""
    is_1022 = code.startswith("13-1022")
    # A bid the company RECEIVES (a salvage buyer's bid, a supplier's bid) is buy-side
    # and must not trip M1; only a bid or quote going out to a customer does.
    sell_side_bid = re.search(
        r"\b(?:bid|quote|quotation|proposal)\b[^.\n]{0,80}\b(?:to|for)\s+(?:the\s+)?"
        r"(?:customer|account|owner|contractor|school|district|city|county|job)|"
        r"\b(?:bid|quote|quotation)\s+(?:package|letter|sheet|form|response)|"
        r"\b(?:price|quote|bid)\s+(?:this|the)\s+(?:job|work|project)|"
        r"\bwhat we (?:would |should )?(?:bid|quote)\b|\bbid (?:it|this) at\b",
        ptext, re.I)
    if is_1022 and sell_side_bid:
        emit("ERROR", "[M1] occupation 13-1022 (buy-side) with a customer-bid prompt - O*NET "
                     "compliance failed this pairing on task 08; consider 41-4012.00")
    if is_1022:
        _check_occupation_frame(ptext)
    picks = meta.get("onet_tasks") or []
    if not picks:
        return
    for line in picks:
        low = line.lower()
        for pat, level, label, signal in ONET_TASK_FIT:
            if not re.search(pat, low):
                continue
            if not re.search(signal, ptext, re.I):
                emit(level, f"[M2] O*NET task pick \"{line[:60]}...\" is about {label}, "
                            "and the prompt carries no signal of it — the platform's Skills "
                            "prompt relevance check reads each pick against the prompt and "
                            "FAILs the whole section on a poor fit (task 13, 2026-08-20)")
            break
