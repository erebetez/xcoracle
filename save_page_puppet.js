'use strict';

const fs = require('fs');
const puppeteer = require('puppeteer');
const xmlserializer = require('xmlserializer');

var html2xhtml = function (htmlString) {
    var parser = require('parse5'),
        dom = parser.parse(htmlString);
 
    return xmlserializer.serializeToString(dom);
};

(async() => {

const browser = await puppeteer.launch({
    executablePath: '/bin/chromium'
    ,headless: false
   });
const page = await browser.newPage();

await page.goto('http://www.xcontest.org/switzerland/de/fluge/tageswertung-pg/#filter[date]=2018-05-12', {waitUntil: 'networkidle0'}); //networkidle0 domcontentloaded


console.log("Loaded!")


//const flights = await page.$('#flights');

//let bodyHTML = await page.evaluate(() => document.body.innerHTML);

await page.screenshot({path: 'example.png'});

var xhtml = html2xhtml(document.body.innerHTML);

await fs.write('1.html', xhtml, 'w');
//page.$(selector)

await browser.close();

})(); 
