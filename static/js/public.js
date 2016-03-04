/**
 * Created by lenovo on 2015/9/24.
 */
/**
 * Created by lenovo on 2015/9/24.
 */
// JavaScript Document
(function (doc, win) {
    var docEl = doc.documentElement,
        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
        recalc = function () {
            var clientWidth = docEl.clientWidth;

            if (!clientWidth) return;
            docEl.style.fontSize = 100 * (clientWidth / 500) + 'px';

        };

    if (!doc.addEventListener) return;
    win.addEventListener(resizeEvt, recalc, false);
    doc.addEventListener('DOMContentLoaded', recalc, false);
})(document, window);/**
 * Created by lenovo on 2015/9/25.
 */
