import{c as g,_ as A,u as q,a as D,o as P,r as B,b as s,d as o,e,f as v,w as E,g as m,t as h,h as w,i as H,H as K,S as U,j as p,E as b,k as f,l as O,v as R,m as G,F as M,n as S,p as V,q as j,s as J,x as z}from"./index-kadmElH5.js";import{f as F,p as Q}from"./index-CrvkQCy0.js";/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const W=g("headphones",[["path",{d:"M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3",key:"1xhozi"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const X=g("image",[["rect",{width:"18",height:"18",x:"3",y:"3",rx:"2",ry:"2",key:"1m3agn"}],["circle",{cx:"9",cy:"9",r:"2",key:"af1f0g"}],["path",{d:"m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21",key:"1xmnt7"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Y=g("laptop",[["path",{d:"M18 5a2 2 0 0 1 2 2v8.526a2 2 0 0 0 .212.897l1.068 2.127a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45l1.068-2.127A2 2 0 0 0 4 15.526V7a2 2 0 0 1 2-2z",key:"1pdavp"}],["path",{d:"M20.054 15.987H3.946",key:"14rxg9"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Z=g("loader-circle",[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ee=g("package-open",[["path",{d:"M12 22v-9",key:"x3hkom"}],["path",{d:"M15.17 2.21a1.67 1.67 0 0 1 1.63 0L21 4.57a1.93 1.93 0 0 1 0 3.36L8.82 14.79a1.655 1.655 0 0 1-1.64 0L3 12.43a1.93 1.93 0 0 1 0-3.36z",key:"2ntwy6"}],["path",{d:"M20 13v3.87a2.06 2.06 0 0 1-1.11 1.83l-6 3.08a1.93 1.93 0 0 1-1.78 0l-6-3.08A2.06 2.06 0 0 1 4 16.87V13",key:"1pmm1c"}],["path",{d:"M21 12.43a1.93 1.93 0 0 0 0-3.36L8.83 2.2a1.64 1.64 0 0 0-1.63 0L3 4.57a1.93 1.93 0 0 0 0 3.36l12.18 6.86a1.636 1.636 0 0 0 1.63 0z",key:"12ttoo"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const te=g("search",[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ae=g("smartphone",[["rect",{width:"14",height:"20",x:"5",y:"2",rx:"2",ry:"2",key:"1yt0o3"}],["path",{d:"M12 18h.01",key:"mhygvu"}]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const se=g("tablet",[["rect",{width:"16",height:"20",x:"4",y:"2",rx:"2",ry:"2",key:"76otgf"}],["line",{x1:"12",x2:"12.01",y1:"18",y2:"18",key:"1dp563"}]]),oe={class:"product-image"},ne={class:"img-ph"},ce={key:0,class:"product-cat-tag"},re=["title"],le={class:"product-body"},ie={class:"product-name"},de={class:"product-meta"},ue={class:"product-price"},pe={class:"product-stock"},ve={__name:"ProductCard",props:{product:{type:Object,required:!0}},emits:["click"],setup(l){const i=l,d=q(),r=D(),n=p(!1);async function y(){var c,k;if(!d.isLoggedIn){b.warning("请先登录再收藏");return}try{n.value?(await F.remove(i.product.id),n.value=!1,b.success("已取消收藏")):(await F.add(i.product.id),n.value=!0,b.success("已收藏"))}catch(C){b.error(((k=(c=C.response)==null?void 0:c.data)==null?void 0:k.detail)||"操作失败")}}function _(){r.addItem(i.product),b.success("已加入购物车")}return P(async()=>{if(d.isLoggedIn)try{const c=await F.check(i.product.id);n.value=c.favorited}catch{}}),(c,k)=>{const C=B("el-image");return s(),o("div",{class:"product-card",onClick:k[0]||(k[0]=L=>c.$emit("click"))},[e("div",oe,[v(C,{src:l.product.image_url,fit:"cover",style:{width:"100%",height:"260px"}},{error:E(()=>[e("div",ne,[v(m(X),{size:32})])]),_:1},8,["src"]),l.product.category?(s(),o("span",ce,h(l.product.category),1)):w("",!0),m(d).isLoggedIn?(s(),o("button",{key:1,class:"product-fav",onClick:H(y,["stop"]),title:n.value?"取消收藏":"收藏"},[v(m(K),{size:16,fill:n.value?"#FF2442":"none",color:n.value?"#FF2442":"#fff","stroke-width":"2"},null,8,["fill","color"])],8,re)):w("",!0),e("button",{class:"product-cart-btn",title:"加入购物车",onClick:H(_,["stop"])},[v(m(U),{size:16,"stroke-width":"1.5"})])]),e("div",le,[e("h3",ie,h(l.product.name),1),e("div",de,[e("span",ue,"¥"+h(l.product.price.toFixed(2)),1),e("span",pe,h(l.product.stock>0?"在售":"缺货"),1)])])])}}},he=A(ve,[["__scopeId","data-v-ad14eaf2"]]),ge={class:"dw-page"},ye={class:"hero-section"},ke={class:"hero-content"},me={class:"hero-search"},fe={class:"hero-search-box"},_e={class:"hero-hints"},Ce=["onClick"],be={class:"categories-section"},we={class:"categories-scroll"},xe=["onClick"],$e={key:0,class:"result-bar"},ze={key:1,class:"dw-loading"},Le={key:2,class:"dw-empty-state"},Me={key:3,class:"product-grid"},Se={key:4,class:"pagination-bar"},Fe={__name:"Home",setup(l){const i=p([]),d=p(!1),r=p(""),n=p(""),y=p(1),_=p(12),c=p(0),k=[{name:"手机",icon:z(ae)},{name:"笔记本",icon:z(Y)},{name:"耳机",icon:z(W)},{name:"平板",icon:z(se)}],C=["华为 手机","笔记本","耳机 降噪","苹果"];function L(u){n.value=u,y.value=1,$()}function x(){y.value=1,$()}function N(u){r.value=u,x()}async function $(){d.value=!0;try{const u=await Q.list({page:y.value,page_size:_.value,keyword:r.value||void 0,category:n.value||void 0});i.value=u.items,c.value=u.total}catch{}d.value=!1}return P($),(u,t)=>{const T=B("el-pagination");return s(),o("div",ge,[e("section",ye,[e("div",ke,[t[5]||(t[5]=e("span",{class:"hero-badge"},"AI 驱动 · 口碑分析",-1)),t[6]||(t[6]=e("h1",{class:"hero-title"},[f("发现好物，"),e("br"),f("从真实评论开始")],-1)),t[7]||(t[7]=e("p",{class:"hero-desc"},[f("智能情感分析帮你快速了解每件商品的真实口碑，"),e("br"),f("不再被虚假评价迷惑")],-1)),e("div",me,[e("div",fe,[v(m(te),{size:18,class:"search-icon"}),O(e("input",{"onUpdate:modelValue":t[0]||(t[0]=a=>r.value=a),placeholder:"搜索商品名称...",class:"hero-search-input",onKeyup:G(x,["enter"])},null,544),[[R,r.value]]),r.value?(s(),o("button",{key:0,class:"hero-clear",onClick:t[1]||(t[1]=a=>{r.value="",x()})},"✕")):w("",!0)]),e("button",{class:"hero-btn",onClick:x},"搜索")]),e("div",_e,[t[4]||(t[4]=e("span",{class:"hint-label"},"热门搜索：",-1)),(s(),o(M,null,S(C,a=>e("button",{key:a,class:"hint-tag",onClick:I=>N(a)},h(a),9,Ce)),64))])])]),e("section",be,[e("div",we,[e("button",{class:V(["cat-btn",{active:n.value===""}]),onClick:t[2]||(t[2]=a=>L(""))},"全部",2),(s(),o(M,null,S(k,a=>e("button",{key:a.name,class:V(["cat-btn",{active:n.value===a.name}]),onClick:I=>L(a.name)},[(s(),j(J(a.icon),{size:16,"stroke-width":"1.5"})),e("span",null,h(a.name),1)],10,xe)),64))])]),r.value&&!d.value?(s(),o("div",$e,[e("p",null,[t[8]||(t[8]=f('搜索 "',-1)),e("strong",null,h(r.value),1),f('" 共 '+h(c.value)+" 个结果",1)])])):w("",!0),d.value?(s(),o("div",ze,[v(m(Z),{class:"is-loading",size:28}),t[9]||(t[9]=e("p",null,"加载中...",-1))])):i.value.length===0?(s(),o("div",Le,[v(m(ee),{size:48}),t[10]||(t[10]=e("p",null,"暂无商品",-1))])):(s(),o("div",Me,[(s(!0),o(M,null,S(i.value,a=>(s(),j(he,{key:a.id,product:a,onClick:I=>u.$router.push(`/product/${a.id}`)},null,8,["product","onClick"]))),128))])),c.value>_.value?(s(),o("div",Se,[v(T,{"current-page":y.value,"onUpdate:currentPage":t[3]||(t[3]=a=>y.value=a),"page-size":_.value,total:c.value,layout:"prev, pager, next",background:"",onCurrentChange:$},null,8,["current-page","page-size","total"])])):w("",!0)])}}},Ve=A(Fe,[["__scopeId","data-v-f0c1acb5"]]);export{Ve as default};
