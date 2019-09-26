window.getSourcename = function (sourceId) {
    switch (sourceId) {
        case 0:
            return "benign";
        case 1:
            return "document.location.href";
        case 2:
            return "document.location.pathname";
        case 3:
            return "document.location.search";
        case 4:
            return "document.location.hash";
        case 5:
            return "document.URL";
        case 6:
            return "document.documentURI";
        case 7:
            return "document.baseURI";
        case 8:
            return "document.cookie";
        case 9:
            return "document.referrer";
        case 10:
            return "document.domain";
        case 11:
            return "window.name";
        case 12:
            return "postMessage";
        case 13:
            return "localStorage";
        case 14:
            return "sessionStorage";
        case 255:
            return "unknown";
        default:
            return "unknown code" + sourceId;
    }
};

window.getSourceInfo = function (source, value, start, end) {
    var sourcePart = value.substring(start, end);

    if (source === 255) {
        var hasEscaping = 0;
        var hasEncodeURI = 0;
        var hasEncodeURIComponent = 0;
        var realSource = source;
        var isSameFrame = 1;
        var sourcename = getSourcename(realSource);
    } else {
        var hasEscaping = (source >> 4) & 1;
        var hasEncodeURI = (source >> 5) & 1;
        var hasEncodeURIComponent = (source >> 6) & 1;
        var realSource = source & 15;
        var sourcename = getSourcename(realSource);
        var isSameFrame = 1;
        if (source >> 7 == 1) // MSB is set to 1
            isSameFrame = 0;
    }

    return {
        "sourceId": realSource,
        "sourceName": sourcename,
        "start": start,
        "end": end,
        "hasEscaping": hasEscaping,
        "hasEncodeURI": hasEncodeURI,
        "hasEncodeURIComponent": hasEncodeURIComponent,
        "sourcePart": sourcePart,
        "isSameFrame": isSameFrame
    };
};

window.repackSources = function (value, sources) {
    let sourceInfo;
    var repackedSources = {};
    var oldsource = sources[0];
    var start = 0;
    var end = 0;
    var x;
    if (typeof(sources) == 'string')
        sources = JSON.parse(sources);
    for (var i = 0; i < sources.length; i++) {
        var source = sources[i];

        if (source !== oldsource) {
            end = i;

            sourceInfo = getSourceInfo(oldsource, value, start, i);
            if (parseInt(start) > -1 && parseInt(end) > -1)
                repackedSources[start] = sourceInfo;

            start = i;
        }

        oldsource = source;
        x = i;
    }
    sourceInfo = getSourceInfo(oldsource, value, start, parseInt(x) + 1);

    if (parseInt(start) > -1 && parseInt(x) > -1)
        repackedSources[start] = sourceInfo;


    return repackedSources;
};

window.___DOMXSSFinderReport = function (sinkId, value, sources, details, loc) {
    // typically, details contains additional information about a sink. For example, sink ID 1
    // is eval-like sinks, so it would have additional information if instead Function, setTimeout, or setInterval was invoked
    // for details on sink IDs see https://github.com/cispa/persistent-clientside-xss/blob/master/src/constants/sources.py

    var finding = {
        location: document.location.href.toString(),
        domain: document.domain,
        taintedValue: value, // String - value of the (parially) tainted string
        sources: sources, // Array  - byte-wise identification of the sources that composed the string
        sinkType: sinkType, // ID - eval, innnerHTML, document.write, ...
        sinkDetails: {
            d1: detail1,
            d2: detail2,
            d3: detail3
        }, // String - Context infos how the source was called, value depends on sinkType
        stringID: 0
    };

    sinkTypeToName = {
        '1': 'eval',
        '2': 'document.write',
        '3': 'innerHTML',
        '5': 'script.text',
        '8': 'script.src',
    };

    console.log("%cTainted flow to sink " + sinkTypeToName[sinkId] + " found!", "font-weight: bold");
    console.log("Value: " + value);
    console.log("Code location: " + detail3);
    var buffer = "";
    var args = Array();
    var s = repackSources(value, sources);
    for (var e in s) {
        var css = "color: black";
        if (s[e].sourceId !== 0 && s[e].sourceId !== 255) {
            css = "color: red";
        }
        buffer += "%c%s";
        args.push(css);
        var text = s[e].sourcePart;
        if (text.indexOf("http") > -1) {
            text = text.replace("://", ":__");
            text = text.replace(".", "_")
        }
        args.push(text)
    }

    args.unshift(buffer);
    console.log.apply(console, args);
};