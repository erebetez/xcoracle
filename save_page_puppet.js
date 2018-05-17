'use strict';

const puppeteer = require('puppeteer');

(async() => {

const browser = await puppeteer.launch({
    executablePath: '/bin/chromium',
    headless: false
   });
const page = await browser.newPage();

await page.goto('http://www.xcontest.org/switzerland/de/fluge/tageswertung-pg/#filter[date]=2018-05-12', {waitUntil: 'networkidle0'}); //networkidle0 domcontentloaded


//let bodyHTML = await page.evaluate(() => document.body.innerHTML);
console.log("HEY!!!!")

//new XMLSerializer().serializeToString(document.doctype) + document.documentElement.outerHTML;

//const flights = await page.$('#flights');
await page.screenshot({path: 'example.png'});


//page.$(selector)

//await browser.close();

})(); 
