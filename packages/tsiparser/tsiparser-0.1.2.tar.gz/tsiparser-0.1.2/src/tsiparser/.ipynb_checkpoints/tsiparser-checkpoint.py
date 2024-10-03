import pandas as pnd
import cobra



def get_db(logger, inexceldb):
    
    logger.debug("Reading the preovided excel file (--inexceldb)...")
    try: exceldb = pnd.ExcelFile(inexceldb)
    except: 
        logger.error(f"The file {inexceldb} does not exist or it is not in a valid format.")
        return 1
    
    
    logger.debug("Checking table presence...")
    sheet_names = exceldb.sheet_names
    for i in ['R', 'M', 'authors']: 
        if i not in sheet_names:
            logger.error(f"Sheet '{i}' is missing!")
            return 1
        
        
    logger.debug("Loading the tables...")
    db = {}
    db['R'] = exceldb.parse('R')
    db['M'] = exceldb.parse('M')
    db['authors'] = exceldb.parse('authors')
    
    
    logger.debug("Checking table headers...")
    headers = {}
    headers['R'] = ['rid', 'rstring', 'kr', 'gpr_manual', 'name', 'author', 'notes']
    headers['M'] = ['pure_mid', 'formula', 'charge', 'kc', 'name', 'inchikey', 'author', 'notes']
    headers['authors'] = ['username', 'first_name', 'last_name', 'role', 'mail']
    for i in db.keys(): 
        if set(db[i].columns) != set(headers[i]):
            logger.error(f"Sheet '{i}' is missing the columns {set(headers[i]) - set(db[i].columns)}.")
            return 1
        
    return db
    


    
def introduce_metabolites(logger, db, model):
    
    
    logger.debug("Checking duplicated metabolite IDs...")
    if len(set(db['M']['pure_mid'].to_list())) != len(db['M']): 
        pure_mids = db['M']['pure_mid'].to_list()
        duplicates = list(set([item for item in pure_mids if pure_mids.count(item) > 1]))
        logger.error(f"Sheet 'M' has duplicated metabolites: {duplicates}.")
        return 1
   
        
    # parse M:
    logger.debug("Parsing metabolites...")
    db['M'] = db['M'].set_index('pure_mid', drop=True, verify_integrity=True)
    for pure_mid, row in db['M'].iterrows():
        
        
        if pnd.isna(row['formula']):
            logger.error(f"Metabolite {pure_mid} has invalid formula: {row['formula']}.")
            return 1
  

        if pnd.isna(row['charge']): 
            logger.error(f"Metabolite {pure_mid} has invalid charge: {row['charge']}.")
            return 1
        
        
        if row['author'] not in db['authors']['username'].to_list(): 
            logger.error(f"Metabolite {pure_mid} has invalid author: {row['author']}.")
            return 1
        
        
        # check 'kc'
        # TODO
        
        
        # add metabolite to model
        m = cobra.Metabolite(f'{pure_mid}_c')
        model.add_metabolites([m])
        m = model.metabolites.get_by_id(f'{pure_mid}_c')
        m.formula = row['formula']
        m.charge = row['charge']
        m.compartment='c'
        
        
    return model
    
    
    
def introduce_reactions(logger, db, model): 
    
    
    logger.debug("Checking duplicated reaction IDs...")
    if len(set(db['R']['rid'].to_list())) != len(db['R']): 
        pure_mids = db['R']['rid'].to_list()
        duplicates = list(set([item for item in pure_mids if pure_mids.count(item) > 1]))
        logger.error(f"Sheet 'R' has duplicated reactions: {duplicates}.")
        return 1
    
        
    # parse R:
    logger.debug("Parsing reactions...")
    db['R'] = db['R'].set_index('rid', drop=True, verify_integrity=True)
    for rid, row in db['R'].iterrows():
        
        
        if ' --> ' not in row['rstring'] and ' <=> ' not in row['rstring']:
            logger.error(f"Reaction {rid} has invalid arrow: {row['rstring']}.")
            return 1
        
        
        if row['author'] not in db['authors']['username'].to_list(): 
            logger.error(f"Metabolite {pure_mid} has invalid author: {row['author']}.")
            return 1
  

        # check 'kr'
        # TODO
        
        
        # add reaction to model
        r = cobra.Reaction(rid)
        model.add_reactions([r])
        r = model.reactions.get_by_id(rid)
        r.build_reaction_from_string(row['rstring'])
        for m in r.metabolites:
            if m.formula == None or m.charge == None:
                logger.error(f"Metabolite {m.id} appears in {r.id} but was not previously defined.")
                return 1
               
        
        # check if unbalanced
        if r.check_mass_balance() != {}: 
            logger.error(f"Reaction {r.id} is unbalanced: {r.check_mass_balance()}.")
            return 1
        
    
    # understand which pw/md are completed, which are missing
    # TODO
    
    
    # parse gpr_manual
    # TODO
    
    
    return model
    
    
    
def tsiparser(args, logger): 
    
    
    # check file structure
    db = get_db(logger, args.inexceldb)
    if type(db)==int: return 1
                                    
        
    # create the model
    model = cobra.Model('tsiparser_uni')
        
    
    model = introduce_metabolites(logger, db, model)
    if type(model)==int: return 1


    model = introduce_reactions(logger, db, model)
    if type(model)==int: return 1    
        
    
    # output the universe
    logger.debug("Creating 'uni.json' in the current directory...")
    cobra.io.save_json_model(model, 'newuni.json')
    
    
    
    return 0