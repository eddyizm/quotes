'''
view constants for api usage. 
'''
RANDOM_QUOTE = '''
    select quotes.quote AS quote, 
        quotes.author as author,			
        quotes.id AS id,
        quotes.category as category
        from quotes offset random() * (select count(*) from quotes) limit 1;
    '''