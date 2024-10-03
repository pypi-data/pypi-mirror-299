settings = {
    'BOT_NAME': 'indeed',
    'SPIDER_MODULES': ['indeed.spiders'],
    'NEWSPIDER_MODULE': 'indeed.spiders',
    
    # Log level (optional if you want to reduce logging verbosity)
    'LOG_LEVEL': 'WARNING',  
    
    # ScrapeOps configuration
    'SCRAPEOPS_API_KEY': 'get_your_own_key',  # Replace with your actual ScrapeOps API Key
    'SCRAPEOPS_PROXY_ENABLED': True,

    # Obey robots.txt rules
    'ROBOTSTXT_OBEY': False,

    # Item pipeline
    'ITEM_PIPELINES': {
        "indeed.pipelines.RawDataPipeline": 200,
    },

    # Downloader middlewares
    'DOWNLOADER_MIDDLEWARES': {
        # ScrapeOps Retry Middleware
        'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,

        # ScrapeOps Proxy Middleware
        'indeed.middlewares.ScrapeOpsProxyMiddleware': 725,
    },

    # ScrapeOps monitoring extension
    'EXTENSIONS': {
        'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
    },

    # Concurrency settings (adapt based on your ScrapeOps plan)
    'CONCURRENT_REQUESTS': 1,  # Max concurrency on ScrapeOps Free Plan is 1 thread
    
    # Additional configurations for Scrapy (Optional - similar to your reference format)
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
    'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    'FEED_EXPORT_ENCODING': "utf-8",
}
