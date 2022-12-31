var oYear = document.querySelector('#year');
var oHours = document.querySelector('#hours');
var oTime = document.querySelector('#time');

function fnUpdateYearCells()
{
    var sHTML = ``;
    var sTitle = '';
    var iM = 0;
    var iDY = 0;
    var oDate = (new Date);
    var sCurDate = oDate.getFullYear()+'-'+(oDate.getMonth()+1)+'-'+(oDate.getDate());

    for (var iY=0; iY<2; iY++) {
        // 6*7 = 24*10 row > cell-group > cell
        // 6*7 = 24*10
        // 6*7 = 24*10
        // 6*7 = 24*10

        var sRowHTML = '';

        // for (var iK=0; iK<5; iK++) {
            var sRow2HTML = '';

            for (var iJ=0; iJ<12; iJ++) {
                var sCellGroupHTML = '';
                var sDate = oDate.getFullYear()+'-'+(iJ+1)+'-'+1;
                var oMonthDate = (new Date(sDate));
                // oDate.setMonth(iM);
                sTitle = oMonthDate.toLocaleString('RU-ru', { month: 'long' });

                for (var iD=1; iD<32; iD++) {
                    var sDate = oMonthDate.getFullYear()+'-'+(oMonthDate.getMonth()+1)+'-'+iD;
                    var oDayDate = (new Date(sDate));
                    console.log(sDate);
                    // oDate.setDate(iD);
                    // var sN = oDate.toLocaleString('RU-ru', { day: 'numeric' });
                    var iCD = oDayDate.getDay()-1;
                    if (iCD==-1) {
                        iCD = 6;
                    }
                    if (iD==1 && 0<iCD) {
                        for (var iC=0; iC<iCD; iC++) {
                            sCellGroupHTML += `<div class="empty"></div>`;
                        }
                    }
                    var sCur = sCurDate==sDate ? "current" : "";
                    console.log([`<div class="day day-${iCD} day-${sDate} ${sCur}">${iN}</div>`, sCur, sCurDate==sDate, sCurDate, sDate]);
                    var iN = oDayDate.getDate();
                    if (iD!=iN) break;
                    sCellGroupHTML += `<div class="day day-${iCD} day-${sDate} ${sCur}">${iN}</div>`;
                }

                sRow2HTML += `<div class="month"><div class="title">${sTitle}</div>${sCellGroupHTML}</div>`;
                iM++;
            }

            // sRowHTML += `<div class="half-year">${sRow2HTML}</div>`;
        // }

        // sHTML += `<div class="row">${sRow2HTML}</div>`;
        sHTML = sRow2HTML;
    }

    oYear.innerHTML = sHTML;

    setTimeout(fnUpdateYearCells, 60000);
}

function fnUpdateDateTime()
{
    var sHTML = ``;
    var oDate = new Date()

    var aHours = []

    var iCurrentHour = oDate.getHours();
    
    aHours = aHours.concat(Array.from({length: 8}, (_, i) => i + 1))
    aHours = aHours.concat(Array.from({length: 8}, (_, i) => i + 9))
    aHours = aHours.concat(Array.from({length: 8}, (_, i) => i + 17 > 23 ? i - 7 : i + 17 ))

    var iCurrentHourIndex = aHours.indexOf(iCurrentHour);

    for (var [iIndex, iHour] of Object.entries(aHours)) {
        var sClass = iIndex < iCurrentHourIndex ? "filled" : ""
        sClass = iIndex == iCurrentHourIndex ? "current" : sClass
        sHTML += `<div class="${sClass}">${iHour}</div>`
    }
    oHours.innerHTML = sHTML;

    sHTML = oDate.toLocaleString('RU-RU', { weekday: "long", day:"2-digit", month:"2-digit", year: "2-digit", hour: "2-digit", minute: "2-digit" });
    oTime.innerHTML = sHTML;

    setTimeout(fnUpdateDateTime, 1000);
}

fnUpdateDateTime();
fnUpdateYearCells();