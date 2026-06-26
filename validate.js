const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();
        
        // Listen to console errors
        page.on('console', msg => {
            if (msg.type() === 'error') console.log('BROWSER_ERROR:', msg.text());
        });
        
        page.on('pageerror', err => {
            console.log('PAGE_ERROR:', err.toString());
        });

        // Use absolute path
        await page.goto(`file://${__dirname}/docs/index.html`, { waitUntil: 'networkidle0' });
        
        const gapText = await page.$eval('#gapText', el => el.textContent);
        const scoreOleg = await page.$eval('#scoreOleg', el => el.textContent);
        const scoreAlex = await page.$eval('#scoreAlex', el => el.textContent);

        console.log("Validation Results:");
        console.log("Gap Text:", gapText);
        console.log("Score Oleg:", scoreOleg);
        console.log("Score Alex:", scoreAlex);
        
        await browser.close();
    } catch (e) {
        console.error("Puppeteer Script Error:", e);
    }
})();
