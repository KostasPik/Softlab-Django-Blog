var content_titles = document.querySelectorAll('.article-body .article-body-title');
    
    async function mainToc(){
        mainTableOfContentsHtml = `<ul>`;
        for(var i=0; i<content_titles.length; ++i) {
        if (content_titles[i].tagName == "H2")
        mainTableOfContentsHtml += `<li class="toc-h2"><a onClick="scrolll(${i})">${content_titles[i].textContent}</a></li>`;
        else if (content_titles[i].tagName == "H3") 
        mainTableOfContentsHtml += `<li class="toc-h3"><a onClick="scrolll(${i})">${content_titles[i].textContent}</a></li>`;
    }
    mainTableOfContentsHtml += "</ul>";
        return mainTableOfContentsHtml
    }

    async function secToc(){
        secTableOfContentsHtml = `<ul>`;
        for(var j = 0; j < content_titles.length; ++j){
            if (content_titles[j].tagName == 'H2')
            secTableOfContentsHtml += `<li class="toc-h2"><a onClick="scrolll(${j})">${content_titles[j].textContent}</a></li>`;
        }
        secTableOfContentsHtml += `</ul>`
        return secTableOfContentsHtml
    }

    async function makeToc(){
        var mainTocHtml = await mainToc();
        var secTocHtml = await secToc();

        if (content_titles.length > 0) {

        var tocTable = document.getElementsByClassName('table-of-contents')
        tocTable[0].innerHTML += mainTocHtml;
        tocTable[1].innerHTML += secTocHtml;
        document.querySelector('.table-of-contents').hidden=false;
        document.getElementsByClassName("table-of-contents")[1].hidden=false;
        }
    }

    makeToc();

    function scrolll(value) {
        var element = document.querySelectorAll('.article-body .article-body-title')[value];
        element.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
    }