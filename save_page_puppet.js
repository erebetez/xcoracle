'use strict';

const fs = require('fs');
const puppeteer = require('puppeteer');

const xcontest_url = 'http://www.xcontest.org/switzerland/de/fluge/tageswertung-pg/'

async function get_flights_by_date(date) {

const browser = await puppeteer.launch({
    executablePath: '/bin/chromium'
    ,headless: false
   });
const page = await browser.newPage();

await page.goto(xcontest_url + '#filter[date]=' + date, {waitUntil: 'networkidle0'});

console.log("Loaded!")

var page_content = await page.content();

await browser.close();

return page_content;
}; 




get_flights_by_date('2018-05-13')
 .catch(e => console.log(e))
 .then(page_content => {
  fs.writeFile('2018-05-13.html', page_content, ((err) => {if(err){console.log(err)}}));
});

