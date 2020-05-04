(function(e){function t(t){for(var r,n,i=t[0],c=t[1],l=t[2],m=0,f=[];m<i.length;m++)n=i[m],Object.prototype.hasOwnProperty.call(o,n)&&o[n]&&f.push(o[n][0]),o[n]=0;for(r in c)Object.prototype.hasOwnProperty.call(c,r)&&(e[r]=c[r]);u&&u(t);while(f.length)f.shift()();return a.push.apply(a,l||[]),s()}function s(){for(var e,t=0;t<a.length;t++){for(var s=a[t],r=!0,i=1;i<s.length;i++){var c=s[i];0!==o[c]&&(r=!1)}r&&(a.splice(t--,1),e=n(n.s=s[0]))}return e}var r={},o={app:0},a=[];function n(t){if(r[t])return r[t].exports;var s=r[t]={i:t,l:!1,exports:{}};return e[t].call(s.exports,s,s.exports,n),s.l=!0,s.exports}n.m=e,n.c=r,n.d=function(e,t,s){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:s})},n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var s=Object.create(null);if(n.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(s,r,function(t){return e[t]}.bind(null,r));return s},n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/static/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=t,i=i.slice();for(var l=0;l<i.length;l++)t(i[l]);var u=c;a.push([0,"chunk-vendors"]),s()})({0:function(e,t,s){e.exports=s("56d7")},"034f":function(e,t,s){"use strict";var r=s("64a9"),o=s.n(r);o.a},"56d7":function(e,t,s){"use strict";s.r(t);s("cadf"),s("551c"),s("f751"),s("097d");var r=s("2b0e"),o=s("5f5b"),a=(s("f9e3"),s("2dd8"),function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{attrs:{id:"app"}},[s("router-view")],1)}),n=[],i=(s("034f"),s("2877")),c={},l=Object(i["a"])(c,a,n,!1,null,null,null),u=l.exports,m=s("8c4f"),f=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{attrs:{id:"home-page"}},[s("GlobalHeader"),s("GlobalMessage"),s("main",{staticClass:"container"},[s("p",{staticClass:"h5 mb-4"},[e._v("ホーム")]),s("b-form",{on:{submit:function(t){return t.preventDefault(),e.submitSave(t)}}},[s("div",{staticClass:"row form-group"},[s("label",{staticClass:"col-sm-3 col-form-label"},[e._v("タイトル")]),s("div",{staticClass:"col-sm-8"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.form.book.title,expression:"form.book.title"}],staticClass:"form-control",attrs:{type:"text"},domProps:{value:e.form.book.title},on:{input:function(t){t.target.composing||e.$set(e.form.book,"title",t.target.value)}}})])]),s("div",{staticClass:"row form-group"},[s("label",{staticClass:"col-sm-3 col-form-label"},[e._v("価格")]),s("div",{staticClass:"col-sm-8"},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.form.book.price,expression:"form.book.price"}],staticClass:"form-control",attrs:{type:"text"},domProps:{value:e.form.book.price},on:{input:function(t){t.target.composing||e.$set(e.form.book,"price",t.target.value)}}})])]),s("div",{staticClass:"row text-center mt-5"},[s("div",{staticClass:"col-sm-12"},[s("b-button",{attrs:{type:"submit",variant:"primary"}},[e._v(e._s(e.isCreated?"更新":"登録"))])],1)])])],1)],1)},d=[],g=(s("ac6a"),s("8615"),s("bc3a")),p=s.n(g),h=s("2f62");r["default"].use(h["a"]);var v={strict:!1,namespaced:!0,state:{username:"",isLoggedIn:!1},getters:{username:function(e){return e.username},isLoggedIn:function(e){return e.isLoggedIn}},mutations:{set:function(e,t){e.username=t.user.username,e.isLoggedIn=!0},clear:function(e){e.username="",e.isLoggedIn=!1}},actions:{login:function(e,t){return y.post("/auth/jwt/create/",{username:t.username,password:t.password}).then(function(t){return localStorage.setItem("access",t.data.access),e.dispatch("reload").then(function(e){return e})})},logout:function(e){localStorage.removeItem("access"),e.commit("clear")},reload:function(e){return y.get("/auth/users/me/").then(function(t){var s=t.data;return e.commit("set",{user:s}),s})}}},b={strict:!1,namespaced:!0,state:{error:"",warnings:[],info:""},getters:{error:function(e){return e.error},warnings:function(e){return e.warnings},info:function(e){return e.info}},mutations:{set:function(e,t){t.error&&(e.error=t.error),t.warnings&&(e.warnings=t.warnings),t.info&&(e.info=t.info)},clear:function(e){e.error="",e.warnings=[],e.info=""}},actions:{setErrorMessage:function(e,t){e.commit("clear"),e.commit("set",{error:t.message})},setWarningMessages:function(e,t){e.commit("clear"),e.commit("set",{warnings:t.messages})},setInfoMessage:function(e,t){e.commit("clear"),e.commit("set",{info:t.message})},clearMessages:function(e){e.commit("clear")}}},w=new h["a"].Store({modules:{auth:v,message:b}}),_=w,C=p.a.create({baseURL:"/api/v1/",timeout:5e3,headers:{"Content-Type":"application/json","X-Requested-With":"XMLHttpRequest"}});C.interceptors.request.use(function(e){_.dispatch("message/clearMessages");var t=localStorage.getItem("access");return t?(e.headers.Authorization="JWT "+t,e):e},function(e){return Promise.reject(e)}),C.interceptors.response.use(function(e){return e},function(e){console.log("error.response=",e.response);var t,s=e.response?e.response.status:500;if(400===s){var r=[].concat.apply([],Object.values(e.response.data));_.dispatch("message/setWarningMessages",{messages:r})}else if(401===s){var o=localStorage.getItem("access");t=null!=o?"ログイン有効期限切れ":"認証エラー",_.dispatch("auth/logout"),_.dispatch("message/setErrorMessage",{message:t})}else 403===s?(t="権限エラーです。",_.dispatch("message/setErrorMessage",{message:t})):(t="想定外のエラーです。",_.dispatch("message/setErrorMessage",{message:t}));return Promise.reject(e)});var y=C,k=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{attrs:{id:"header"}},[s("b-navbar",{attrs:{type:"dark",variant:"dark"}},[s("a",{staticClass:"navbar-brand",attrs:{href:"/"}},[e._v("DRF Sample")]),e.$route.meta.requiresAuth?s("b-navbar-nav",{staticClass:"ml-auto"},[e.isLoggedIn?s("b-nav-item-dropdown",{attrs:{right:""}},[s("template",{slot:"button-content"},[e._v(e._s(e.username))]),s("b-dropdown-item",{attrs:{href:"#"},on:{click:e.clickLogout}},[e._v("ログアウト")])],2):s("b-nav-item",{attrs:{href:"#"},on:{click:e.clickLogin}},[e._v("ログイン")])],1):e._e()],1)],1)},x=[],$=(s("a481"),{computed:{username:function(){return this.$store.getters["auth/username"]},isLoggedIn:function(){return this.$store.getters["auth/isLoggedIn"]}},methods:{clickLogout:function(){this.$store.dispatch("auth/logout"),this.$store.dispatch("message/setInfoMessage",{message:"ログアウトしました。"}),this.$router.replace("/login")},clickLogin:function(){this.$store.dispatch("message/clearMessages"),this.$router.replace("/login")}}}),M=$,j=Object(i["a"])(M,k,x,!1,null,null,null),I=j.exports,L=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{attrs:{id:"messages"}},[s("b-alert",{directives:[{name:"show",rawName:"v-show",value:e.message.error,expression:"message.error"}],staticClass:"mb-0",attrs:{variant:"danger",show:""}},[e._v("\n    "+e._s(e.message.error)+"\n  ")]),s("b-alert",{directives:[{name:"show",rawName:"v-show",value:e.message.warnings.length>0,expression:"message.warnings.length > 0"}],staticClass:"mb-0",attrs:{variant:"warning",show:""}},e._l(e.message.warnings,function(t){return s("p",{staticClass:"mb-0"},[e._v(e._s(t))])}),0),s("b-alert",{directives:[{name:"show",rawName:"v-show",value:e.message.info,expression:"message.info"}],staticClass:"mb-0",attrs:{variant:"info",show:""}},[e._v("\n    "+e._s(e.message.info)+"\n  ")])],1)},O=[],S={computed:{message:function(){return this.$store.state.message}}},P=S,q=Object(i["a"])(P,L,O,!1,null,null,null),E=q.exports,G={components:{GlobalHeader:I,GlobalMessage:E},data:function(){return{form:{book:{title:"",price:0}}}},computed:{isCreated:function(){return void 0!==this.form.book.id}},methods:{submitSave:function(){var e=this;y({method:this.isCreated?"put":"post",url:this.isCreated?"/books/"+this.form.book.id+"/":"/books/",data:{id:this.form.book.id,title:this.form.book.title,price:this.form.book.price}}).then(function(t){var s=e.isCreated?"更新しました。":"登録しました。";e.$store.dispatch("message/setInfoMessage",{message:s}),e.form.book=t.data})}}},T=G,H=Object(i["a"])(T,f,d,!1,null,null,null),N=H.exports,A=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{attrs:{id:"login-page"}},[s("GlobalHeader"),s("GlobalMessage"),s("main",{staticClass:"container"},[s("p",{staticClass:"h5 mb-4"},[e._v("ログイン")]),s("b-form",{on:{submit:function(t){return t.preventDefault(),e.submitLogin(t)}}},[s("div",{staticClass:"row form-group"},[s("label",{staticClass:"col-sm-3 col-form-label"},[e._v("ユーザー名")]),s("div",{staticClass:"col-sm-8"},[s("b-form-input",{attrs:{type:"text",required:""},model:{value:e.form.username,callback:function(t){e.$set(e.form,"username",t)},expression:"form.username"}})],1)]),s("div",{staticClass:"row form-group"},[s("label",{staticClass:"col-sm-3 col-form-label"},[e._v("パスワード")]),s("div",{staticClass:"col-sm-8"},[s("b-form-input",{attrs:{type:"password",required:""},model:{value:e.form.password,callback:function(t){e.$set(e.form,"password",t)},expression:"form.password"}})],1)]),s("div",{staticClass:"row text-center mt-5"},[s("div",{staticClass:"col-sm-12"},[s("b-button",{attrs:{type:"submit",variant:"primary"}},[e._v("ログイン")])],1)])])],1)],1)},R=[],W={components:{GlobalHeader:I,GlobalMessage:E},data:function(){return{form:{username:"",password:""}}},methods:{submitLogin:function(){var e=this;this.$store.dispatch("auth/login",{username:this.form.username,password:this.form.password}).then(function(){console.log("Login succeeded."),e.$store.dispatch("message/setInfoMessage",{message:"ログインしました。"});var t=e.$route.query.next||"/";e.$router.replace(t)})}}},D=W,J=Object(i["a"])(D,A,R,!1,null,null,null),U=J.exports;r["default"].use(m["a"]);var F=new m["a"]({mode:"history",routes:[{path:"/",component:N,meta:{requiresAuth:!0}},{path:"/login",component:U},{path:"*",redirect:"/"}]});function X(e,t,s){console.log("Force user to login page."),s({path:"/login",query:{next:e.fullPath}})}F.beforeEach(function(e,t,s){var r=_.getters["auth/isLoggedIn"],o=localStorage.getItem("access");console.log("to.path=",e.path),console.log("isLoggedIn=",r),e.matched.some(function(e){return e.meta.requiresAuth})?r?(console.log("User is already logged in. So, free to next."),s()):null!=o?(console.log("User is not logged in. Trying to reload again."),_.dispatch("auth/reload").then(function(){console.log("Succeeded to reload. So, free to next."),s()}).catch(function(){X(e,t,s)})):X(e,t,s):(console.log("Go to public page."),s())});var z=F;r["default"].config.productionTip=!0,r["default"].use(o["a"]),new r["default"]({router:z,store:_,render:function(e){return e(u)}}).$mount("#app")},"64a9":function(e,t,s){}});
//# sourceMappingURL=app.063eb2f2.js.map