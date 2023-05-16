"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[158],{3905:(e,t,n)=>{n.d(t,{Zo:()=>m,kt:()=>f});var r=n(7294);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,i=function(e,t){if(null==e)return{};var n,r,i={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var s=r.createContext({}),l=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},m=function(e){var t=l(e.components);return r.createElement(s.Provider,{value:t},e.children)},p="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},d=r.forwardRef((function(e,t){var n=e.components,i=e.mdxType,a=e.originalType,s=e.parentName,m=c(e,["components","mdxType","originalType","parentName"]),p=l(n),d=i,f=p["".concat(s,".").concat(d)]||p[d]||u[d]||a;return n?r.createElement(f,o(o({ref:t},m),{},{components:n})):r.createElement(f,o({ref:t},m))}));function f(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var a=n.length,o=new Array(a);o[0]=d;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c[p]="string"==typeof e?e:i,o[1]=c;for(var l=2;l<a;l++)o[l]=n[l];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}d.displayName="MDXCreateElement"},7711:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>o,default:()=>u,frontMatter:()=>a,metadata:()=>c,toc:()=>l});var r=n(7462),i=(n(7294),n(3905));const a={sidebar_position:3},o="Create a Performance",c={unversionedId:"tutorial-basics/music-performance",id:"tutorial-basics/music-performance",title:"Create a Performance",description:"The realisation of a mmMusicalPerformance, describing a performance that can be either live (mmStudioPerformance).",source:"@site/docs/tutorial-basics/music-performance.md",sourceDirName:"tutorial-basics",slug:"/tutorial-basics/music-performance",permalink:"/music-meta-ontology/docs/tutorial-basics/music-performance",draft:!1,editUrl:"ahttps://github.com/polifonia-project/music-meta-ontology/tree/main/website/docs/tutorial-basics/music-performance.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"Create a Music Entity",permalink:"/music-meta-ontology/docs/tutorial-basics/create-music"},next:{title:"Links and provenance",permalink:"/music-meta-ontology/docs/tutorial-basics/links_provenance"}},s={},l=[{value:"Publication and licensing",id:"publication-and-licensing",level:2}],m={toc:l},p="wrapper";function u(e){let{components:t,...a}=e;return(0,i.kt)(p,(0,r.Z)({},m,a,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"create-a-performance"},"Create a Performance"),(0,i.kt)("p",null,"The realisation of a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:MusicEntity")," is exemplified by ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:MusicalPerformance"),", describing a performance that can be either live (",(0,i.kt)("inlineCode",{parentName:"p"},"mm:LivePerformance"),") or in a studio (",(0,i.kt)("inlineCode",{parentName:"p"},"mm:StudioPerformance"),").\nAs illustrated in the figure below, the place and time interval of a performance are described by ",(0,i.kt)("inlineCode",{parentName:"p"},"core:Place")," and ",(0,i.kt)("inlineCode",{parentName:"p"},"core:TimeInterval")," -- involving one or more ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:MusicArtist"),"s (optionally with a specific role).\nIn turn, a performance may create a new ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:MusicEntity")," if the execution differs significantly from the original version."),(0,i.kt)("p",null,(0,i.kt)("img",{alt:"Example banner",src:n(8556).Z,width:"1743",height:"543"})),(0,i.kt)("p",null,"A Music Entity can also be recorded by means of a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:RecordingProcess"),", which is a subclass of ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:CreativeProcess")," that allows for specifying location, time interval and persons involved in recording the song.\nThis makes it possible to describe information about both the production (e.g., producers) and the technical aspects of it (e.g., sound engineer, equipment used).\nThe recording process produces a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:Recording"),", which is contained in a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:Release"),"."),(0,i.kt)("p",null,"Information about the broadcasting of a recording is modelled through the ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:BroadcastingSituation")," class (an instance of the Situation ODP ","[3]",", which describes when and where the song was broadcast, and by which broadcaster (",(0,i.kt)("inlineCode",{parentName:"p"},"mm:Broadcaster"),")."),(0,i.kt)("h2",{id:"publication-and-licensing"},"Publication and licensing"),(0,i.kt)("p",null,"The ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:PublicationSituation")," class describes information about the publication of a release, which is common to the publication of a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:Score")," (see figure above).\nFor both a release and a score, it describes when and where they were published, and by a ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:Publisher"),"."),(0,i.kt)("p",null,"Licence information is described by the ",(0,i.kt)("inlineCode",{parentName:"p"},"mm:License")," class, which applies to records, releases and scores."))}u.isMDXComponent=!0},8556:(e,t,n)=>{n.d(t,{Z:()=>r});const r=n.p+"assets/images/performance-a5cb0847d55d9451e4ae34bff6b2f36a.png"}}]);