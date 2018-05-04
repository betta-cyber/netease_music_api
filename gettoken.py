#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
from ghost import Ghost

def get_token():
    driver = webdriver.PhantomJS('/Users/shokill/phantomjs') # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get('http://127.0.0.1:8080/gettoken.html')


    submit_button = driver.find_element_by_xpath('//*[@id="submitForm"]/input[3]')
    submit_button.click()

    driver.implicitly_wait(2)

    return driver.find_element_by_xpath('/html/body/p').text

def get_check_token():
    code = """
    (function(){function u(b,a){for(var c in a)b.setAttribute(c,a[c])}function q(b,a){b.onload=function(){this.onerror=this.onload=null;a(null,b)};b.onerror=function(){this.onerror=this.onload=null;a(Error("Failed to load "+this.src),b)}}function v(b,a){b.onreadystatechange=function(){if("complete"==this.readyState||"loaded"==this.readyState)this.onreadystatechange=null,a(null,b)}}function m(){}function p(b,a,c){for(var e in a)!a.hasOwnProperty(e)||void 0!==b[e]&&!0!==c||(b[e]=a[e]);return b}function r(b,
    a,c){var e=function(a){return a.replace(/(^\/)|(\/$)/g,"")};a=e(a.replace(/^https?:\/\//i,""));return(c=c?e(c):"")?b+"://"+a+"/"+c:b+"://"+a}function w(b,a,c){function e(){h.parentNode&&h.parentNode.removeChild(h);window[f]=m;n&&clearTimeout(n)}"function"===typeof a&&(c=a,a={});a||(a={});var d=a.prefix||"__jp",f=a.name||d+x++,d=a.param||"cb",g=null!=a.timeout?a.timeout:6E4;a=encodeURIComponent;var k=document.getElementsByTagName("script")[0]||document.head,h,n;g&&(n=setTimeout(function(){e();c&&c(Error("Timeout"))},
    g));window[f]=function(a){e();c&&c(null,a)};g=(new Date).getTime();b+=(~b.indexOf("?")?"\x26":"?")+d+"\x3d"+a(f)+"\x26t\x3d"+g;b=b.replace("?\x26","?");h=document.createElement("script");h.src=b;k.parentNode.insertBefore(h,k);return function(){window[f]&&e()}}function y(b){try{var a=localStorage.getItem(b).split(l);if(+a.splice(-1)>=t())return a.join(l);localStorage.removeItem(b);return""}catch(c){return""}}function z(b,a){var c=b.pn,e=b.protocol,d=b.timeout,f=b.__serverConfig__;void 0===f&&(f={});
    c=r(e,f.configServer||"ac.dun.163yun.com","/v2/config/js?pn\x3d"+c);w(c,{timeout:d},a)}var A=function(b,a,c){var e=document.head||document.getElementsByTagName("head")[0],d=document.createElement("script");"function"===typeof a&&(c=a,a={});a=a||{};c=c||function(){};d.type=a.type||"text/javascript";d.charset=a.charset||"utf8";d.async="async"in a?!!a.async:!0;d.src=b;a.attrs&&u(d,a.attrs);a.text&&(d.text=""+a.text);("onload"in d?q:v)(d,c);d.onload||q(d,c);e.appendChild(d)},x=0,l=",",t=function(b){void 0===
    b&&(b=0);return(new Date).getTime()+parseInt(b,10)},B=function(b){function a(a,b){var c=a.protocol,g=a.onerror,k=a.__serverConfig__;void 0===k&&(k={});var h=b.split(","),n=h[0],m=h[1],l=h[2],k=p({configHash:l,sConfig:l,staticServer:k.staticServer||n,apiServer:k.apiServer||m,buildVersion:h[3]},a),h=k.buildVersion+"/watchman.min",c=r(c,k.staticServer)+"/"+h+".js";window.WM_CONFIG=k;A(c,{charset:"UTF-8"},function(a){if(a)return g("[NEWatchman] load js file error")})}var c=y("wm_cf");c?a(b,c):z(b,function(c,
    d){var f=b.onerror;if(c)return f(Error("[NEWatchman] fetch config timeout"));if(d&&200===d.code){var g=d.result,f=g.ivp,g=[g.s,g.as,g.conf,g.v].join();try{var k=t(f);localStorage.setItem("wm_cf",g+l+k)}catch(h){}a(b,g)}else f(Error("[NEWatchman] fetch config error"))})};window.initWatchman=window.initNEWatchman=function(b,a,c){var e=b.pn,d=b.productNumber;if(!e&&!d)throw Error("[NEWatchman] required product number");var f=location.protocol.replace(":","");b=p(p({onload:a,onerror:c},b),{protocol:f,
    auto:!0,onload:m,onerror:m,timeout:0,pn:e||d});B(b)}})();
    initWatchman({
        productNumber: 'YD00000558929251',
        onload: function (instance) {
            wm = instance
        }
    });
    function get() {
        wm & wm.getToken('0b0cdd23ed1144a0b78de049edc09824', function(token) { console.log(token); });
    }
    """
    gh = Ghost()
    with ghost.start() as session:
        page, extra_resources = session.open("http://localhost:8080/token.html")
        assert page.http_status == 200 and 'jeanphix' in page.content

    print page, extra_resources

get_check_token()

