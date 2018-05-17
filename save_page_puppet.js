'use strict';

const fs = require('fs');
const puppeteer = require('puppeteer');

(async() => {

const browser = await puppeteer.launch({
    executablePath: '/bin/chromium'
    ,headless: false
   });
const page = await browser.newPage();

await page.goto('http://www.xcontest.org/switzerland/de/fluge/tageswertung-pg/#filter[date]=2018-05-12', {waitUntil: 'networkidle0'}); //networkidle0 domcontentloaded


console.log("Loaded!")


var page_content = await page.content();
//console.log(page_content);


fs.writeFile('1.html', page_content, ((err) => {if(err){console.log(err)}}));

await browser.close();

})(); 
