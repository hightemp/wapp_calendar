var aImpDays = [
    '2023-02-01',
    '2023-03-01',
];

const DAY = 24*60*60*1000;

$(document).ready(() => {
    for (var iY=0; iY<3; iY++) {
        var iCurrentTimestamp = (new Date()).getTime();
        var sY = (new Date()).getFullYear()
        var iCY = sY-1+iY
        var iTimestamp = (new Date(`${iCY}-01-01`)).getTime();
        $("#days").append(`<div class="year-separator">${iCY}</div>`)
        var bFirstday = true;
        var iSpace = 0;

        var oDate = (new Date)
        oDate.setTime(iTimestamp);
        var iCD = oDate.getDay();
        if (iCD==-1) {
            iCD = 6;
        }
        iSpace = iCD-1;
        for (var iD=0; iD<iSpace;iD++) {
            $("#days").append(`<div class="day day-spacer"></div>`)
        }

        for (var iD=0; iD<365;iD++) {
            var iDiffTimestamp = iTimestamp + iD*DAY
            var oDate = (new Date)
            oDate.setTime(iDiffTimestamp);
            var sExtClass = "";
            if (iDiffTimestamp+DAY < iCurrentTimestamp) {
                sExtClass = "day-last";
            }
            for (var sDay of aImpDays) {
                var iDayTimestamp = (new Date(sDay)).getTime();
                console.log(iDayTimestamp, iDiffTimestamp);
                if (Math.round(iDayTimestamp/DAY) == Math.round(iDiffTimestamp/DAY)) {
                    sExtClass = "day-important";
                }
            }
            var iCD = oDate.getDay()-1;
            if (iCD==-1) {
                iCD = 6;
            }
            var sDate = oDate.getFullYear()+'-'+(oDate.getMonth()+1)+'-'+oDate.getDate();
            var sUTC = oDate+'';
            $("#days").append(`<div class="day weekday-${iCD} ${sExtClass}" title="${sUTC}"></div>`)
        }
    }
})