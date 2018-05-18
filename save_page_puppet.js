'use strict';

const fs = require('fs');
const puppeteer = require('puppeteer');
const { spawn } = require('child_process');


const xcontest_url = 'http://www.xcontest.org/switzerland/de/fluge/tageswertung-pg/'

const output_dir = 'fligts'

fs.mkdir(output_dir, ((err) => {if(err){console.log(err)}}))

async function get_flights_by_date(date) {

    const browser = await puppeteer.launch({
        executablePath: '/bin/chromium'
        ,headless: false
    });
    const page = await browser.newPage();

    console.log("get xc list of " + date);

    await page.goto(xcontest_url + '#filter[date]=' + date, {waitUntil: 'networkidle2'});

    console.log("Loaded!");

    let pg = await page.content();

    await browser.close();

    return pg;
}; 

function span_xslt(page_content, cb){
    const xslt = spawn('xsltproc', ['--html', 'clean_flights.xslt', '-']);
    let retr_data = "";

    xslt.stdin.write(page_content);
    xslt.stdin.end();

    xslt.stdout.on('data', (data) => {
      retr_data = retr_data + data;
    });

    xslt.stderr.on('data', (data) => {
      console.log(`stderr: ${data}`);
    });

    xslt.on('close', (code) => {
      if(code === 0){
        cb(retr_data);
      } else {
        throw new Error("xsltproc finished with non zero code: " + code);
      }
    });
}

(async (date) => {
    try {
        let page_content = await get_flights_by_date(date);
//         fs.writeFile(output_dir + '/' + date + '.html', page_content, ((err) => {if(err){console.log(err)}}));

        span_xslt(page_content, ((clean_flights) => {
//           console.log("clean_flights: " + clean_flights);
          fs.writeFile(output_dir + '/' + date + '.xml', clean_flights, ((err) => {if(err){console.log(err)}}));
        }));

    } catch(e) {
        console.log(e);
    }
})('2018-05-14')
