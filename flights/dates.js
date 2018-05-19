'use strict';

Date.prototype.addDays = function(days) {
    let dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
}

Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('-');
};

var getDateArray = function(start, end) {
    var arr = new Array();
    var dt = start;
    while (dt <= end) {
        arr.push(new Date(dt));
        dt.setDate(dt.getDate() + 1);
    }
    return arr;
}

var getDateStringArray = function(start, end){
  return getDateArray(start, end).map((date) => date.yyyymmdd());
}

module.exports = {
   getDateStringArray: getDateStringArray
}
