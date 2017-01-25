# The Diaburu Experimental Web-crawler

Diaburu is an experimental web-crawler intended to support experimental research in information retrieval,
data-intensive text processing, data-mining, user experience, and machine learning. Some propositions for
documents scanning, representation, and retrieval are being turned into code. Nevertheless, this project
is not aimed to turn into a production-ready tool.

## Dependencies

 * Python (tested with 2.6 and 2.7)
 * Ruby (tested with 1.8 and 1.9)

## How to execute

0. First execute the URL Server through

   ```sh
   $ ruby script/server
   ```

1. Then execute the Crawler process through

   ```
   $ python script/crawler
   ```

The Storage Server is not implemented yet; the Crawler process will fetch URLs and send them to the URL
Server but will not persist the HTML (or anything else) from these URL. The Crawler process doesn't
fetch images, scripts, and CSS files, for instance. The first URL to be fetched is
http://en.wikipedia.org/wiki/Main_Page.

## License

Please refer to the included LICENSE file for terms of use.

Apache License, Version 2.0. Copyright 2011-2017 &copy; Ewerton Assis.
