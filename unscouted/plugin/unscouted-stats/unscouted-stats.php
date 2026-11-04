<?php
/*
Plugin Name: Unscouted Stats
Description: First-party funnel tracking for the Unscouted interactives (views, starts, finishes, offer clicks, checkout, orders) and an email list, with an admin dashboard.
Version: 1.0.0
Author: Unscouted
*/
if (!defined('ABSPATH')) exit;

define('USS_VER', '1.0.0');

function uss_t($n){ global $wpdb; return $wpdb->prefix.'us_'.$n; }

/* ---------- install ---------- */
register_activation_hook(__FILE__, 'uss_install');
function uss_install(){
  global $wpdb; require_once ABSPATH.'wp-admin/includes/upgrade.php';
  $c = $wpdb->get_charset_collate();
  dbDelta("CREATE TABLE ".uss_t('events')." (
    id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    ts datetime NOT NULL,
    vid varchar(40) NOT NULL DEFAULT '',
    sid varchar(40) NOT NULL DEFAULT '',
    ev varchar(30) NOT NULL,
    page varchar(150) NOT NULL DEFAULT '',
    pos varchar(16) NOT NULL DEFAULT '',
    val varchar(60) NOT NULL DEFAULT '',
    x varchar(120) NOT NULL DEFAULT '',
    ref varchar(120) NOT NULL DEFAULT '',
    dev varchar(8) NOT NULL DEFAULT '',
    PRIMARY KEY  (id),
    KEY ts (ts),
    KEY ev_ts (ev,ts),
    KEY vid (vid)
  ) $c;");
  dbDelta("CREATE TABLE ".uss_t('emails')." (
    id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    ts datetime NOT NULL,
    email varchar(190) NOT NULL,
    source varchar(30) NOT NULL DEFAULT '',
    detail varchar(255) NOT NULL DEFAULT '',
    ref_id bigint(20) unsigned NOT NULL DEFAULT 0,
    vid varchar(40) NOT NULL DEFAULT '',
    PRIMARY KEY  (id),
    KEY email (email),
    KEY ts (ts),
    KEY src_ref (source,ref_id)
  ) $c;");
  update_option('uss_db', USS_VER);
  uss_backfill_orders();
}
add_action('plugins_loaded', function(){ if (get_option('uss_db') !== USS_VER) uss_install(); });

/* ---------- helpers ---------- */
function uss_is_admin_visitor(){
  if (is_user_logged_in()) return current_user_can('manage_options');
  if (defined('LOGGED_IN_COOKIE') && !empty($_COOKIE[LOGGED_IN_COOKIE])) {
    $uid = wp_validate_auth_cookie($_COOKIE[LOGGED_IN_COOKIE], 'logged_in');
    if ($uid && user_can($uid, 'manage_options')) return true;
  }
  return false;
}
function uss_vid(){ return isset($_COOKIE['us_vid']) ? substr(preg_replace('/[^a-z0-9]/i','',$_COOKIE['us_vid']),0,40) : ''; }
function uss_dev(){ $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : ''; return preg_match('/Mobi|Android|iPhone|iPad/i',$ua) ? 'mobile' : 'desktop'; }
function uss_is_bot(){ $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : ''; return $ua === '' || preg_match('/bot|crawl|spider|slurp|headless|lighthouse|pingdom|preview|facebookexternalhit|curl|wget|python/i',$ua); }
function uss_log($ev, $a = array()){
  global $wpdb;
  $wpdb->insert(uss_t('events'), array(
    'ts'   => current_time('mysql'),
    'vid'  => isset($a['vid']) ? $a['vid'] : uss_vid(),
    'sid'  => isset($a['sid']) ? $a['sid'] : '',
    'ev'   => $ev,
    'page' => isset($a['page']) ? substr($a['page'],0,150) : '',
    'pos'  => isset($a['pos']) ? substr($a['pos'],0,16) : '',
    'val'  => isset($a['val']) ? substr((string)$a['val'],0,60) : '',
    'x'    => isset($a['x']) ? substr((string)$a['x'],0,120) : '',
    'ref'  => isset($a['ref']) ? substr($a['ref'],0,120) : '',
    'dev'  => uss_dev(),
  ));
}
function uss_add_email($email, $source, $detail = '', $ref_id = 0, $vid = ''){
  global $wpdb; $email = strtolower(trim(sanitize_email($email)));
  if (!$email || !is_email($email)) return;
  if ($ref_id && $wpdb->get_var($wpdb->prepare("SELECT id FROM ".uss_t('emails')." WHERE source=%s AND ref_id=%d", $source, $ref_id))) return;
  $wpdb->insert(uss_t('emails'), array('ts'=>current_time('mysql'),'email'=>$email,'source'=>$source,'detail'=>substr($detail,0,255),'ref_id'=>(int)$ref_id,'vid'=>$vid));
}

/* ---------- public event endpoint ---------- */
add_action('rest_api_init', function(){
  register_rest_route('us/v1', '/e', array('methods'=>'POST','permission_callback'=>'__return_true','callback'=>'uss_rest_event'));
  register_rest_route('us/v1', '/email', array('methods'=>'POST','permission_callback'=>'__return_true','callback'=>'uss_rest_email'));
});
function uss_rate_ok($limit){
  $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
  $k = 'uss_rl_'.md5($ip.wp_salt('nonce')); $n = (int)get_transient($k);
  if ($n >= $limit) return false; set_transient($k, $n+1, 600); return true;
}
function uss_body($req){ $d = json_decode($req->get_body(), true); return is_array($d) ? $d : $req->get_params(); }
function uss_rest_event($req){
  if (uss_is_bot() || uss_is_admin_visitor() || !uss_rate_ok(300)) return new WP_REST_Response(array('ok'=>1), 200);
  $d = uss_body($req);
  $ok = array('view','test_start','q_next','test_finish','buy_click','product_click','parent_share','share','again','cta_click','email_submit');
  $ev = isset($d['ev']) ? sanitize_key($d['ev']) : '';
  if (!in_array($ev, $ok, true)) return new WP_REST_Response(array('ok'=>0), 200);
  $c = function($k,$n=120) use ($d){ return isset($d[$k]) ? substr(sanitize_text_field((string)$d[$k]),0,$n) : ''; };
  uss_log($ev, array('vid'=>preg_replace('/[^a-z0-9]/i','',$c('v',40)),'sid'=>preg_replace('/[^a-z0-9]/i','',$c('s',40)),'page'=>$c('p',150),'pos'=>$c('pos',16),'val'=>$c('val',60),'x'=>$c('x',120),'ref'=>$c('r',120)));
  return new WP_REST_Response(array('ok'=>1), 200);
}
function uss_rest_email($req){
  if (uss_is_bot() || !uss_rate_ok(300)) return new WP_REST_Response(array('ok'=>1), 200);
  $d = uss_body($req);
  $em = isset($d['email']) ? $d['email'] : '';
  if (!is_email($em)) return new WP_REST_Response(array('ok'=>0,'error'=>'email'), 400);
  $det = isset($d['detail']) ? sanitize_text_field($d['detail']) : '';
  $src = isset($d['source']) ? sanitize_key($d['source']) : 'form';
  $vid = isset($d['v']) ? preg_replace('/[^a-z0-9]/i','',$d['v']) : uss_vid();
  uss_add_email($em, $src ? $src : 'form', $det, 0, $vid);
  if (!uss_is_admin_visitor()) uss_log('email_submit', array('vid'=>$vid,'page'=>isset($d['p'])?sanitize_text_field($d['p']):'','x'=>$src));
  return new WP_REST_Response(array('ok'=>1), 200);
}

/* ---------- capture emails from other places ---------- */
// Hostinger Reach signup form
add_filter('rest_request_after_callbacks', function($resp, $handler, $req){
  if (strpos($req->get_route(), '/hostinger-reach/v1/contact') === 0) {
    $p = $req->get_json_params(); if (!is_array($p)) $p = $req->get_params();
    if (!empty($p['email'])) uss_add_email($p['email'], 'signup', isset($p['tags']) ? (is_array($p['tags'])?implode(',',$p['tags']):$p['tags']) : '', 0, uss_vid());
  }
  return $resp;
}, 10, 3);
// New WP accounts
add_action('user_register', function($uid){ $u = get_userdata($uid); if ($u) uss_add_email($u->user_email, 'account', 'User #'.$uid, $uid); });
// Orders: tag visitor id + store email
function uss_order_created($order){
  if (is_numeric($order)) $order = wc_get_order($order);
  if (!$order) return;
  $vid = uss_vid(); if ($vid) { $order->update_meta_data('_us_vid', $vid); $order->save(); }
  uss_order_email($order);
}
add_action('woocommerce_checkout_order_created', 'uss_order_created');
add_action('woocommerce_store_api_checkout_order_processed', 'uss_order_created');
function uss_order_items($order){ $n = array(); foreach ($order->get_items() as $it) $n[] = $it->get_name(); return html_entity_decode(implode(' + ', $n)); }
function uss_order_email($order){
  $em = $order->get_billing_email(); if (!$em) return;
  uss_add_email($em, 'order', 'Order #'.$order->get_id().': '.uss_order_items($order).' ($'.$order->get_total().')', $order->get_id(), (string)$order->get_meta('_us_vid'));
}
add_action('woocommerce_order_status_changed', function($id, $from, $to, $order){
  if (!in_array($to, array('processing','completed'), true)) return;
  if ($order->get_meta('_us_logged')) return;
  $order->update_meta_data('_us_logged', 1); $order->save();
  uss_order_email($order);
  $ids = array(); foreach ($order->get_items() as $it) $ids[] = $it->get_product_id();
  global $wpdb;
  $wpdb->insert(uss_t('events'), array('ts'=>current_time('mysql'),'vid'=>(string)$order->get_meta('_us_vid'),'ev'=>'order_paid','page'=>'/checkout/','val'=>(string)$order->get_total(),'x'=>implode(',',$ids),'dev'=>''));
}, 10, 4);
function uss_backfill_orders(){
  if (!function_exists('wc_get_orders')) return;
  $orders = wc_get_orders(array('limit'=>-1,'status'=>array('processing','completed','on-hold','pending'),'orderby'=>'date','order'=>'ASC'));
  global $wpdb;
  foreach ($orders as $o) {
    $em = $o->get_billing_email(); if (!$em) continue;
    if ($wpdb->get_var($wpdb->prepare("SELECT id FROM ".uss_t('emails')." WHERE source='order' AND ref_id=%d", $o->get_id()))) continue;
    $d = $o->get_date_created();
    $wpdb->insert(uss_t('emails'), array('ts'=>$d ? $d->date('Y-m-d H:i:s') : current_time('mysql'),'email'=>strtolower($em),'source'=>'order','detail'=>'Order #'.$o->get_id().': '.uss_order_items($o).' ($'.$o->get_total().')','ref_id'=>$o->get_id(),'vid'=>''));
  }
}
// Checkout page views (server side, catches people who come from any button)
add_action('template_redirect', function(){
  if (!function_exists('is_checkout') || !is_checkout() || is_wc_endpoint_url('order-received')) return;
  if (uss_is_bot() || uss_is_admin_visitor()) return;
  uss_log('checkout_view', array('page'=>'/checkout/'));
});

/* ---------- front-end tracker ---------- */
add_action('wp_footer', function(){
  if (is_admin() || uss_is_admin_visitor()) return;
  ?>
<script id="us-stats">(function(){try{
if(/bot|crawl|spider|headless|lighthouse|preview/i.test(navigator.userAgent))return;
var E='/wp-json/us/v1/e',P=location.pathname;
function gid(k,st){try{var v=st.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);st.setItem(k,v)}return v}catch(e){return ''}}
var V=gid('us_vid',localStorage),S=gid('us_sid',sessionStorage);
try{if(V)document.cookie='us_vid='+V+';path=/;max-age=31536000;SameSite=Lax'}catch(e){}
function send(ev,d){d=d||{};var b=JSON.stringify({ev:ev,v:V,s:S,p:P,pos:d.pos||'',val:d.val==null?'':String(d.val),x:d.x||'',r:d.r||''});
 try{if(navigator.sendBeacon){if(navigator.sendBeacon(E,new Blob([b],{type:'text/plain'})))return}}catch(e){}
 try{fetch(E,{method:'POST',body:b,keepalive:true,credentials:'same-origin',headers:{'Content-Type':'text/plain'}})}catch(e){}}
window.usT=send;
var ref='';try{var q=new URLSearchParams(location.search);ref=q.get('utm_source')||'';if(!ref)if(document.referrer)if(document.referrer.indexOf(location.host)<0)ref=document.referrer.split('/')[2]||''}catch(e){}
send('view',{r:ref});
function $(i){return document.getElementById(i)}
function pos(){var b=document.querySelector('#ust-pos button.on,#ust-s-diff button.on,#ust-s-diff .on');return b?(b.getAttribute('data-p')||b.getAttribute('data-d')||b.textContent||'').trim().slice(0,16):''}
document.addEventListener('click',function(e){var t=e.target.closest?e.target.closest('button,a'):null;if(!t)return;var i=t.id||'',h=t.getAttribute('href')||'';
 if(i=='ust-start'||i=='ust-all'||i=='ust-s-start'){send('test_start',{pos:pos(),x:i=='ust-all'?'all20':''});return}
 if(i=='ust-next'||i=='ust-s-next'){var n=($(i=='ust-next'?'ust-n':'ust-s-n')||{}).textContent||'';send('q_next',{pos:pos(),val:parseInt(n,10)||0});return}
 if(t.hasAttribute('data-buy')){send('buy_click',{pos:pos(),val:t.getAttribute('data-buy')});return}
 if(i=='ust-parentBtn'){send('parent_share',{pos:pos()});return}
 if(i=='ust-shareBtn'||i=='ust-copyBtn'||i=='ust-s-share'){send('share',{pos:pos(),x:i});return}
 if(i=='ust-again'||i=='ust-s-again'||i=='ust-other'||i=='ust-s-change'){send('again',{pos:pos(),x:i});return}
 if(h.indexOf('add-to-cart=')>-1){send('buy_click',{pos:pos(),val:(h.match(/add-to-cart=(\d+)/)||[])[1]||'',x:'link'});return}
 if(h.indexOf('/product/')>-1){send('product_click',{val:h.replace(/^https?:\/\/[^\/]+/,'').slice(0,60)});return}
 if(t.closest('#ust,#ust-s,.us-cta,.wp-block-button')){if(h)send('cta_click',{val:h.replace(/^https?:\/\/[^\/]+/,'').slice(0,60),x:(t.textContent||'').trim().slice(0,60)})}
},true);
function watch(id,cls,scoreId,weakSel){var el=$(id);if(!el)return;var was=el.classList.contains(cls);
 new MutationObserver(function(){var h=el.classList.contains(cls);if(was)if(!h){var sc=(($(scoreId)||{}).textContent||'').replace(/\s/g,'');var w=document.querySelector(weakSel);send('test_finish',{pos:pos(),val:sc,x:w?w.textContent.trim().slice(0,60):''})}was=h}).observe(el,{attributes:true,attributeFilter:['class']})}
function init(){watch('ust-res','hide','ust-pts','#ust-weak b');watch('ust-s-res','ust-hide','ust-s-score','#ust-s-band')}
if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',init);else init();
}catch(e){}})();</script>
<?php
}, 99);

/* ---------- admin ---------- */
add_action('admin_menu', function(){
  add_menu_page('Unscouted Stats', 'Unscouted Stats', 'manage_options', 'unscouted-stats', 'uss_page', 'dashicons-chart-bar', 3);
});
add_action('admin_post_uss_csv', function(){
  if (!current_user_can('manage_options')) wp_die('no');
  check_admin_referer('uss_csv');
  global $wpdb;
  $rows = $wpdb->get_results("SELECT email, MIN(ts) first_seen, MAX(ts) last_seen, GROUP_CONCAT(DISTINCT source) sources, COUNT(*) n, SUBSTRING_INDEX(GROUP_CONCAT(detail ORDER BY ts DESC SEPARATOR '||'),'||',1) last_detail FROM ".uss_t('emails')." GROUP BY email ORDER BY first_seen DESC", ARRAY_A);
  header('Content-Type: text/csv; charset=utf-8');
  header('Content-Disposition: attachment; filename=unscouted-emails-'.date('Y-m-d').'.csv');
  $o = fopen('php://output','w'); fputcsv($o, array('email','first_seen','last_seen','sources','entries','last_detail'));
  foreach ($rows as $r) fputcsv($o, $r); fclose($o); exit;
});

function uss_pname($id){
  static $c = array(); if (isset($c[$id])) return $c[$id];
  $n = '#'.$id; if (function_exists('wc_get_product')) { $p = wc_get_product((int)$id); if ($p) $n = html_entity_decode($p->get_name()).' ($'.$p->get_price().')'; }
  return $c[$id] = $n;
}
function uss_pct($a,$b){ return $b ? round(100*$a/$b).'%' : '–'; }

function uss_page(){
  if (!current_user_can('manage_options')) return;
  global $wpdb; $E = uss_t('events'); $M = uss_t('emails');
  $ranges = array('1'=>'Today','7'=>'7 days','30'=>'30 days','90'=>'90 days','3650'=>'All time');
  $d = isset($_GET['d']) ? (string)(int)$_GET['d'] : '30'; if (!isset($ranges[$d])) $d = '30';
  $now = current_time('timestamp');
  $since = $d === '1' ? date('Y-m-d 00:00:00', $now) : date('Y-m-d H:i:s', $now - ((int)$d)*86400);
  $test = isset($_GET['tp']) ? sanitize_text_field($_GET['tp']) : '/soccer-iq-test/';
  $q = function($sql) use ($wpdb){ return $wpdb->get_var($sql); };
  $uv = function($ev, $page = null) use ($wpdb, $E, $since){
    $s = $wpdb->prepare("SELECT COUNT(DISTINCT IF(vid='',CONCAT('s',id),vid)) FROM $E WHERE ev=%s AND ts>=%s", $ev, $since);
    if ($page !== null) $s .= $wpdb->prepare(" AND page=%s", $page);
    return (int)$wpdb->get_var($s);
  };
  // site
  $visitors = (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT vid) FROM $E WHERE ev='view' AND ts>=%s", $since));
  $views = (int)$q($wpdb->prepare("SELECT COUNT(*) FROM $E WHERE ev='view' AND ts>=%s", $since));
  // free test funnel
  $f_view = $uv('view', $test); $f_start = $uv('test_start', $test); $f_fin = $uv('test_finish', $test);
  $f_click = (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT vid) FROM $E WHERE ev IN ('buy_click','parent_share') AND page=%s AND ts>=%s", $test, $since));
  $f_co = (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT c.vid) FROM $E c WHERE c.ev='checkout_view' AND c.ts>=%s AND c.vid<>'' AND c.vid IN (SELECT vid FROM $E WHERE ev='test_finish' AND page=%s AND vid<>'')", $since, $test));
  $f_buy = (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT c.vid) FROM $E c WHERE c.ev='order_paid' AND c.ts>=%s AND c.vid<>'' AND c.vid IN (SELECT vid FROM $E WHERE ev='test_finish' AND page=%s AND vid<>'')", $since, $test));
  $co_all = $uv('checkout_view');
  // orders
  $orders = array(); $rev = 0; $paid = 0; $free = 0;
  if (function_exists('wc_get_orders')) {
    $orders = wc_get_orders(array('limit'=>200,'status'=>array('processing','completed','on-hold','pending','failed','cancelled','refunded'),'date_created'=>'>='.strtotime(get_gmt_from_date($since)),'orderby'=>'date','order'=>'DESC'));
    foreach ($orders as $o) { if (in_array($o->get_status(), array('processing','completed'), true)) { if ($o->get_total() > 0) { $paid++; $rev += (float)$o->get_total(); } else $free++; } }
  }
  $em_new = (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT email) FROM $M WHERE ts>=%s", $since));
  $em_all = (int)$q("SELECT COUNT(DISTINCT email) FROM $M");
  // offers
  $clicks = $wpdb->get_results($wpdb->prepare("SELECT ev, val, page, COUNT(*) n, COUNT(DISTINCT vid) u FROM $E WHERE ev IN ('buy_click','parent_share','share','product_click','cta_click','again') AND ts>=%s GROUP BY ev,val,page ORDER BY n DESC LIMIT 40", $since));
  // drop-off
  $drop = $wpdb->get_results($wpdb->prepare("SELECT CAST(val AS UNSIGNED) k, COUNT(DISTINCT vid) u FROM $E WHERE ev='q_next' AND page=%s AND ts>=%s GROUP BY k ORDER BY k", $test, $since), OBJECT_K);
  $maxq = 0; foreach ($drop as $k=>$r) if ($k > $maxq) $maxq = $k;
  // positions
  $posrows = $wpdb->get_results($wpdb->prepare("SELECT pos, SUM(ev='test_start') s, SUM(ev='test_finish') f, AVG(IF(ev='test_finish', CAST(SUBSTRING_INDEX(val,'/',1) AS DECIMAL(5,2)), NULL)) a, SUM(ev='buy_click') b FROM $E WHERE page=%s AND ts>=%s AND ev IN ('test_start','test_finish','buy_click') GROUP BY pos ORDER BY s DESC", $test, $since));
  $scores = $wpdb->get_results($wpdb->prepare("SELECT val, COUNT(*) n FROM $E WHERE ev='test_finish' AND page=%s AND ts>=%s GROUP BY val ORDER BY CAST(SUBSTRING_INDEX(val,'/',1) AS UNSIGNED)", $test, $since));
  $weak = $wpdb->get_results($wpdb->prepare("SELECT x, COUNT(*) n FROM $E WHERE ev='test_finish' AND page=%s AND ts>=%s AND x<>'' GROUP BY x ORDER BY n DESC LIMIT 15", $test, $since));
  // interactives
  $tools = $wpdb->get_results($wpdb->prepare("SELECT page, COUNT(DISTINCT IF(ev='view',vid,NULL)) v, COUNT(DISTINCT IF(ev='test_start',vid,NULL)) s, COUNT(DISTINCT IF(ev='test_finish',vid,NULL)) f, SUM(ev='test_finish') fr, COUNT(DISTINCT IF(ev='buy_click',vid,NULL)) b FROM $E WHERE ts>=%s AND page IN (SELECT DISTINCT page FROM $E WHERE ev='test_start' AND ts>=%s) GROUP BY page ORDER BY s DESC", $since, $since));
  $pages = $wpdb->get_results($wpdb->prepare("SELECT page, COUNT(*) n, COUNT(DISTINCT vid) u FROM $E WHERE ev='view' AND ts>=%s GROUP BY page ORDER BY u DESC LIMIT 25", $since));
  $refs = $wpdb->get_results($wpdb->prepare("SELECT ref, COUNT(DISTINCT vid) u FROM $E WHERE ev='view' AND ts>=%s AND ref<>'' GROUP BY ref ORDER BY u DESC LIMIT 15", $since));
  $devs = $wpdb->get_results($wpdb->prepare("SELECT dev, COUNT(DISTINCT vid) u FROM $E WHERE ev='view' AND ts>=%s GROUP BY dev", $since));
  $days = $wpdb->get_results($wpdb->prepare("SELECT DATE(ts) dd, COUNT(DISTINCT IF(ev='view',vid,NULL)) v, COUNT(DISTINCT IF(ev='test_start',vid,NULL)) s, COUNT(DISTINCT IF(ev='test_finish',vid,NULL)) f, COUNT(DISTINCT IF(ev IN ('buy_click','parent_share'),vid,NULL)) c, COUNT(DISTINCT IF(ev='checkout_view',vid,NULL)) co, SUM(ev='order_paid') o FROM $E WHERE ts>=%s GROUP BY dd ORDER BY dd DESC LIMIT 60", $since));
  $emails = $wpdb->get_results("SELECT email, MIN(ts) first_seen, GROUP_CONCAT(DISTINCT source) sources, COUNT(*) n, SUBSTRING_INDEX(GROUP_CONCAT(detail ORDER BY ts DESC SEPARATOR '||'),'||',1) detail FROM $M GROUP BY email ORDER BY first_seen DESC LIMIT 500");
  $first = $q("SELECT MIN(ts) FROM $E");
  $base = admin_url('admin.php?page=unscouted-stats');
  $testpages = $wpdb->get_col("SELECT DISTINCT page FROM $E WHERE ev='test_start'"); if (!in_array('/soccer-iq-test/', $testpages, true)) array_unshift($testpages, '/soccer-iq-test/');
  ?>
  <style>
  .uss{max-width:1200px;font-size:14px}.uss h1{font-size:26px;margin:18px 0 4px}.uss h2{font-size:18px;margin:34px 0 10px}
  .uss .sub{color:#646970;margin:0 0 14px}.uss .rng a{display:inline-block;padding:6px 12px;border:1px solid #c3c4c7;border-radius:6px;margin:0 6px 6px 0;text-decoration:none;background:#fff;color:#1d2327}
  .uss .rng a.on{background:#1d2327;color:#fff;border-color:#1d2327}
  .uss .kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
  .uss .k{background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:14px 16px}.uss .k b{display:block;font-size:26px;line-height:1.2;color:#1d2327}.uss .k span{color:#646970;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
  .uss .k em{font-style:normal;color:#646970;font-size:12px}
  .uss .fun{background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:16px}
  .uss .fr{display:grid;grid-template-columns:230px 1fr 140px;gap:12px;align-items:center;margin:8px 0}
  .uss .bar{background:#f0f0f1;border-radius:6px;height:26px;overflow:hidden}.uss .bar i{display:block;height:100%;background:#7ab317;border-radius:6px;min-width:2px}
  .uss .fr .n{font-weight:700}.uss .fr .n em{font-weight:400;color:#646970;font-style:normal;margin-left:6px}
  .uss .grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:900px){.uss .grid2{grid-template-columns:1fr}.uss .fr{grid-template-columns:140px 1fr 110px}}
  .uss table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #dcdcde;border-radius:10px;overflow:hidden}
  .uss th,.uss td{padding:8px 10px;border-bottom:1px solid #f0f0f1;text-align:left;vertical-align:top}.uss th{background:#f6f7f7;font-weight:600}
  .uss td.r,.uss th.r{text-align:right}.uss .note{background:#fcf9e8;border:1px solid #f0e3a8;border-radius:8px;padding:10px 14px;margin:10px 0}
  .uss .tp select{margin-left:6px}
  </style>
  <div class="wrap uss">
  <h1>Unscouted Stats</h1>
  <p class="sub">Your own first-party numbers. Your admin visits are not counted. Tracking started <?php echo $first ? esc_html(date('M j, Y H:i', strtotime($first))) : 'just now'; ?>; orders and emails include older data from WooCommerce.</p>
  <div class="rng"><?php foreach ($ranges as $k=>$l) echo '<a class="'.($k===$d?'on':'').'" href="'.esc_url(add_query_arg(array('d'=>$k,'tp'=>$test),$base)).'">'.esc_html($l).'</a>'; ?></div>

  <div class="kp" style="margin-top:12px">
    <div class="k"><span>Visitors</span><b><?php echo $visitors; ?></b><em><?php echo $views; ?> page views</em></div>
    <div class="k"><span>Started a test</span><b><?php echo (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT vid) FROM $E WHERE ev='test_start' AND ts>=%s",$since)); ?></b><em>any interactive</em></div>
    <div class="k"><span>Finished a test</span><b><?php echo (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT vid) FROM $E WHERE ev='test_finish' AND ts>=%s",$since)); ?></b><em><?php echo (int)$q($wpdb->prepare("SELECT COUNT(*) FROM $E WHERE ev='test_finish' AND ts>=%s",$since)); ?> finishes total</em></div>
    <div class="k"><span>Clicked an offer</span><b><?php echo (int)$q($wpdb->prepare("SELECT COUNT(DISTINCT vid) FROM $E WHERE ev='buy_click' AND ts>=%s",$since)); ?></b><em>buy buttons</em></div>
    <div class="k"><span>Reached checkout</span><b><?php echo $co_all; ?></b><em>people</em></div>
    <div class="k"><span>Paid orders</span><b><?php echo $paid; ?></b><em><?php echo $free; ?> free orders</em></div>
    <div class="k"><span>Revenue</span><b>$<?php echo number_format($rev, 2); ?></b><em>processing + completed</em></div>
    <div class="k"><span>Emails</span><b><?php echo $em_new; ?></b><em><?php echo $em_all; ?> on the list in total</em></div>
  </div>

  <h2>Free test funnel <span class="tp" style="font-weight:400;font-size:13px">
    <form method="get" style="display:inline"><input type="hidden" name="page" value="unscouted-stats"><input type="hidden" name="d" value="<?php echo esc_attr($d); ?>">
    <select name="tp" onchange="this.form.submit()"><?php foreach ($testpages as $tp) echo '<option '.selected($tp,$test,false).' value="'.esc_attr($tp).'">'.esc_html($tp).'</option>'; ?></select></form></span></h2>
  <div class="fun">
  <?php
  $steps = array(
    array('Opened the test page', $f_view),
    array('Started the test', $f_start),
    array('Finished (saw result)', $f_fin),
    array('Clicked unlock / parent', $f_click),
    array('Reached checkout', $f_co),
    array('Bought', $f_buy),
  );
  $top = max(1, $steps[0][1]); $prev = null;
  foreach ($steps as $s) {
    echo '<div class="fr"><div>'.esc_html($s[0]).'</div><div class="bar"><i style="width:'.min(100, round(100*$s[1]/$top)).'%"></i></div><div class="n">'.$s[1].'<em>'.($prev===null?'':uss_pct($s[1],$prev).' of prev').'</em></div></div>';
    $prev = $s[1];
  }
  ?>
  <p class="sub" style="margin:10px 0 0">People = unique devices. "Reached checkout" and "Bought" count only people who also finished this test.</p>
  </div>

  <div class="grid2">
  <div>
    <h2>Where people stop (free test)</h2>
    <table><tr><th>Answered situation</th><th class="r">People</th><th class="r">Of starters</th></tr>
    <?php if (!$drop) echo '<tr><td colspan="3">No data yet</td></tr>'; for ($k=1; $k<=$maxq; $k++) { $u = isset($drop[$k]) ? (int)$drop[$k]->u : 0; echo '<tr><td>'.$k.'</td><td class="r">'.$u.'</td><td class="r">'.uss_pct($u,$f_start).'</td></tr>'; } ?>
    </table>
  </div>
  <div>
    <h2>Offer and share clicks</h2>
    <table><tr><th>What</th><th>Page</th><th class="r">Clicks</th><th class="r">People</th></tr>
    <?php if (!$clicks) echo '<tr><td colspan="4">No clicks yet</td></tr>';
    $lab = array('buy_click'=>'Buy: ','parent_share'=>'Send to parent','share'=>'Share score','product_click'=>'Product link: ','cta_click'=>'Button: ','again'=>'Play again');
    foreach ($clicks as $c) { $w = $lab[$c->ev]; if ($c->ev==='buy_click') $w .= uss_pname($c->val); elseif ($c->ev==='product_click' || $c->ev==='cta_click') $w .= $c->val;
      echo '<tr><td>'.esc_html($w).'</td><td>'.esc_html($c->page).'</td><td class="r">'.(int)$c->n.'</td><td class="r">'.(int)$c->u.'</td></tr>'; } ?>
    </table>
  </div>
  </div>

  <div class="grid2">
  <div>
    <h2>By position (<?php echo esc_html($test); ?>)</h2>
    <table><tr><th>Position</th><th class="r">Starts</th><th class="r">Finishes</th><th class="r">Avg score</th><th class="r">Buy clicks</th></tr>
    <?php if (!$posrows) echo '<tr><td colspan="5">No data yet</td></tr>'; foreach ($posrows as $r) echo '<tr><td>'.esc_html($r->pos ? $r->pos : '–').'</td><td class="r">'.(int)$r->s.'</td><td class="r">'.(int)$r->f.'</td><td class="r">'.($r->a!==null?number_format((float)$r->a,1):'–').'</td><td class="r">'.(int)$r->b.'</td></tr>'; ?>
    </table>
  </div>
  <div>
    <h2>Scores and weak spots</h2>
    <table><tr><th>Score</th><th class="r">Finishes</th></tr>
    <?php if (!$scores) echo '<tr><td colspan="2">No data yet</td></tr>'; foreach ($scores as $r) echo '<tr><td>'.esc_html($r->val).'</td><td class="r">'.(int)$r->n.'</td></tr>'; ?>
    </table>
    <table style="margin-top:12px"><tr><th>Weakest skill shown</th><th class="r">Times</th></tr>
    <?php if (!$weak) echo '<tr><td colspan="2">No data yet</td></tr>'; foreach ($weak as $r) echo '<tr><td>'.esc_html($r->x).'</td><td class="r">'.(int)$r->n.'</td></tr>'; ?>
    </table>
  </div>
  </div>

  <h2>All interactives</h2>
  <table><tr><th>Page</th><th class="r">Visitors</th><th class="r">Started</th><th class="r">Finished</th><th class="r">Finish rate</th><th class="r">Total finishes</th><th class="r">Clicked buy</th></tr>
  <?php if (!$tools) echo '<tr><td colspan="7">No data yet</td></tr>'; foreach ($tools as $r) echo '<tr><td>'.esc_html($r->page).'</td><td class="r">'.(int)$r->v.'</td><td class="r">'.(int)$r->s.'</td><td class="r">'.(int)$r->f.'</td><td class="r">'.uss_pct($r->f,$r->s).'</td><td class="r">'.(int)$r->fr.'</td><td class="r">'.(int)$r->b.'</td></tr>'; ?>
  </table>
  <p class="sub">The hidden drills-… pages are the paid versions, so starts there are customers using what they bought.</p>

  <h2>Day by day</h2>
  <table><tr><th>Date</th><th class="r">Visitors</th><th class="r">Started</th><th class="r">Finished</th><th class="r">Offer clicks</th><th class="r">Checkout</th><th class="r">Orders</th></tr>
  <?php if (!$days) echo '<tr><td colspan="7">No data yet</td></tr>'; foreach ($days as $r) echo '<tr><td>'.esc_html($r->dd).'</td><td class="r">'.(int)$r->v.'</td><td class="r">'.(int)$r->s.'</td><td class="r">'.(int)$r->f.'</td><td class="r">'.(int)$r->c.'</td><td class="r">'.(int)$r->co.'</td><td class="r">'.(int)$r->o.'</td></tr>'; ?>
  </table>

  <div class="grid2">
  <div>
    <h2>Top pages</h2>
    <table><tr><th>Page</th><th class="r">Visitors</th><th class="r">Views</th></tr>
    <?php if (!$pages) echo '<tr><td colspan="3">No data yet</td></tr>'; foreach ($pages as $r) echo '<tr><td>'.esc_html($r->page).'</td><td class="r">'.(int)$r->u.'</td><td class="r">'.(int)$r->n.'</td></tr>'; ?>
    </table>
  </div>
  <div>
    <h2>Where visitors come from</h2>
    <table><tr><th>Source</th><th class="r">Visitors</th></tr>
    <?php if (!$refs) echo '<tr><td colspan="2">No outside referrers yet (direct visits are not listed)</td></tr>'; foreach ($refs as $r) echo '<tr><td>'.esc_html($r->ref).'</td><td class="r">'.(int)$r->u.'</td></tr>'; ?>
    </table>
    <table style="margin-top:12px"><tr><th>Device</th><th class="r">Visitors</th></tr>
    <?php foreach ($devs as $r) echo '<tr><td>'.esc_html($r->dev ? $r->dev : '–').'</td><td class="r">'.(int)$r->u.'</td></tr>'; ?>
    </table>
  </div>
  </div>

  <h2>Orders (<?php echo esc_html($ranges[$d]); ?>)</h2>
  <table><tr><th>Date</th><th>Order</th><th>Status</th><th>Email</th><th>Items</th><th class="r">Total</th></tr>
  <?php if (!$orders) echo '<tr><td colspan="6">No orders in this range</td></tr>';
  foreach ($orders as $o) { $dc = $o->get_date_created(); echo '<tr><td>'.esc_html($dc ? $dc->date_i18n('M j, H:i') : '').'</td><td><a href="'.esc_url($o->get_edit_order_url()).'">#'.$o->get_id().'</a></td><td>'.esc_html(wc_get_order_status_name($o->get_status())).'</td><td>'.esc_html($o->get_billing_email()).'</td><td>'.esc_html(uss_order_items($o)).'</td><td class="r">$'.esc_html($o->get_total()).'</td></tr>'; } ?>
  </table>

  <h2>Email list (<?php echo $em_all; ?>) <a class="button" style="margin-left:10px" href="<?php echo esc_url(wp_nonce_url(admin_url('admin-post.php?action=uss_csv'), 'uss_csv')); ?>">Download CSV</a></h2>
  <p class="sub">Every email from orders (including the free PDF), new accounts, the signup form and any future email form that posts to <code>/wp-json/us/v1/email</code>. Newest first.</p>
  <table><tr><th>Email</th><th>First seen</th><th>Source</th><th>Latest</th></tr>
  <?php if (!$emails) echo '<tr><td colspan="4">No emails yet</td></tr>'; foreach ($emails as $r) echo '<tr><td>'.esc_html($r->email).'</td><td>'.esc_html(date('M j, Y', strtotime($r->first_seen))).'</td><td>'.esc_html($r->sources).'</td><td>'.esc_html($r->detail).'</td></tr>'; ?>
  </table>
  </div>
  <?php
}
