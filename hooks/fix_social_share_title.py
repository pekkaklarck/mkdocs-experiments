def on_page_context(context, page, config, nav):
    for meta in page.meta['meta']:
        if meta.get('property') == 'og:title' and meta.get('content') == 'Welcome':
            meta['content'] = 'Robot Framework Manual'
