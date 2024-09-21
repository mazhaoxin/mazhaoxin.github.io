// ZhaoxinMa @2022/7/31
// 用该工具可以根据网址自动生成后续网址。
// 给网站设置好阅读模式，可以避免广告影响。

'use strict';

const CHAPTERS = 30;
const PAGES = 3;

function main(){
    // full = ?URL=escaped_URL
    let full = unescape(window.location.search);
    if(full.length==0 || full=='?' || full=='?URL='){
        let form = document.querySelector("#config_form");
        if(form){
            form.style.display = "block";
        }
    }
    else{
        let main = document.querySelector('#main');
        if(!main) return;
        let ul = document.createElement('UL');
        ul.className = 'list-group'
        main.appendChild(ul);

        // a = ['?URL=https', '', 'm.xxx.com', 'book', '(book_no)', '(chapter_no).html']
        let a = full.split('/');
        if(a.length == 6){
            a[0] = a[0].substr(5, 999); // remove "?URL="
            let b = a[5];               // '(chapter_no).html'
            let c = b.split('.');       // ['(chapter_no)', 'html']
            let d = c[0].split('_');    // ['(chapter)', '[no]']

            let ch_no = parseInt(d[0]); // (chapter)
            let postfix = '.'+c[1];     // '.html'
            for(let i=0; i<CHAPTERS; i++){
                for(let j=1; j<=PAGES; j++){
                    a[5] = ''+(ch_no+i)+((j==1)?'':('_'+j))+postfix;

                    let li = document.createElement('LI');
                    li.className = 'list-group-item';
                    let link = document.createElement('A');
                    link.textContent = a[5];
                    link.href = a.join('/');
                    li.appendChild(link);
                    ul.appendChild(li);
                }
            }
            a[5] = ''+(ch_no+CHAPTERS)+postfix;
            let link = document.createElement('A');
            link.textContent = 'Next '+CHAPTERS+' Chapters >>>';
            link.href = '?URL='+a.join('/');
            main.appendChild(link);
        }
    }
}