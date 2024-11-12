company = "Apple"
tt = """Donald Trump has claimed he received a phone call on Thursday from Apple's chief executive Tim Cook, in which the tech boss shared concerns about the European Union. He says Mr Cook told him he was concerned about recent financial penalties issued by the EU, which ordered Apple to pay Ireland €13bn (£11bn; $14bn) in unpaid taxes in September. Mr Trump, who is running as the Republican candidate for the upcoming US Presidential Election, made the claim in a podcast released on Thursday. The BBC has asked Apple for a response. Mr Trump told presenter Patrick Bet-David in his appearance on the PBD Podcast that Mr Cook had called him a few hours prior to complain about fines the company was forced to pay after breaching EU rules. He said Mr Cook had told him about a recent $15bn fine from the EU, to which Mr Trump said he responded "that's a lot". "Then on top of that, they got fined by the European Union another $2bn," Mr Trump continued, "so it's a $17-18bn fine." Apple and the Irish government lost a long-running legal dispute over unpaid taxes in September. The EU's highest court upheld an accusation by the bloc's legislative arm, the European Commission, that Ireland gave Apple illegal tax advantages. Mr Cook described the Commission's findings as "political" and said Ireland was being "picked on" in 2016. The European Commission fined Apple €1.8bn several months earlier in March for allegedly breaking music streaming rules, in a win for rival service Spotify. According to Mr Trump, the Apple chief executive went on to make a remark about the EU using the money received via antitrust fines to run an "enterprise". Antitrust fines paid by firms which breach EU competition rules go towards the bloc's general budget and "help to finance the EU and reduce the burden for taxpayers," the Commission's website states. A Commission spokesperson said antitrust fines are designed to sanction companies that have breached competition rules, as well as deter them and others from engaging in anti-competitive behaviour. "When determining the amount of the fine, the Commission considers both the gravity and the duration of the infringement," they told BBC News. "All companies are welcome in the EU, provided they respect our rules and legislation." Mr Trump said he told Mr Cook he would not let the EU "take advantage of our companies", but he needed to "get elected first". The former president has spent some of his campaign trying to woo prominent tech figures, with Tesla and X (formerly Twitter) boss Elon Musk among those backing Mr Trump. He also said he spoke to Google boss Sundar Pichai earlier this week, and claims to have had multiple calls with Meta boss Mark Zuckerberg in August. Mr Musk and the heads of several large tech firms have criticised the EU's approach to regulating their platforms. The bloc has set of rules and requirements that firms must comply with in order to offer digital products and services in the region. These include the General Data Protection Regulation (GDPR), and its Digital Markets Act (DMA) and Digital Services Act. Its two digital laws aim to rein in powerful "gatekeeper" tech companies, provide more choice for consumers and protect users of online platforms or services from illegal or harmful content. Apple has previously claimed that opening up services including its app store to third parties, as required by the DMA, could be bad for users. The EU's Artificial Intelligence (AI) Act, passed earlier this year, also created concern for some tech firms in regulating products according to their risks. It will also make producers of general purpose AI systems be more transparent about data used to train their models. Meta executive Nick Clegg recently said that "regulatory uncertainty" in the EU was behind the delayed roll out of generative AI products there. Apple has also said its own suite of generative AI features will not be coming to iPhones in the EU when they become immediately available elsewhere."""


from transformers import pipeline

# Load sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(article_text, company_name):
    # Step 1: Filter text mentioning the company
    relevant_text = []
    sentences = article_text.split('.')
    
    for sentence in sentences:
        if company_name.lower() in sentence.lower():
            relevant_text.append(sentence.strip())
    
    # If no relevant text is found, default to full article for analysis
    relevant_text = ' '.join(relevant_text) if relevant_text else article_text

    # Step 2: Perform sentiment analysis
    sentiment_results = sentiment_model(relevant_text)

    # Step 3: Calculate and output the sentiment score
    positive_score = sum(result['score'] for result in sentiment_results if result['label'] == 'POSITIVE')
    negative_score = sum(result['score'] for result in sentiment_results if result['label'] == 'NEGATIVE')
    
    # Normalized score from -1 to 1
    sentiment_score = positive_score - negative_score
    return sentiment_score

score = analyze_sentiment(tt, company)
print(score)