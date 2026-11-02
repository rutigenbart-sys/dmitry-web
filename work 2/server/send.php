<?php
// Приём заявок с сайта -> Telegram. Загрузите на PHP-хостинг рядом с сайтом (НЕ в публичный репозиторий).
// Заполните три константы ниже.
const BOT_TOKEN = 'ВСТАВЬТЕ_ТОКЕН_БОТА';   // от @BotFather
const CHAT_ID   = 'ВСТАВЬТЕ_CHAT_ID';       // ваш id (узнать у @userinfobot)
const ORIGIN    = 'https://dmitry-web.ru';  // разрешённый источник запросов

header('Content-Type: application/json; charset=utf-8');
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin === ORIGIN || $origin === 'https://www.dmitry-web.ru') {
  header('Access-Control-Allow-Origin: ' . $origin);
  header('Vary: Origin');
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }

$raw = file_get_contents('php://input', false, null, 0, 20000);
$d = json_decode($raw, true);
if (!is_array($d)) { http_response_code(400); echo '{"ok":false}'; exit; }

// Антиспам: honeypot и слишком быстрая отправка — молча «успех»
if (!empty($d['website']) || (isset($d['t']) && (int)$d['t'] < 1200)) { echo '{"ok":true}'; exit; }

// Лимит: не чаще 1 заявки в 20 секунд с одного IP
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$f = sys_get_temp_dir() . '/lead_' . md5($ip);
if (is_file($f) && time() - filemtime($f) < 20) { http_response_code(429); echo '{"ok":false}'; exit; }
touch($f);

$text = trim((string)($d['text'] ?? ''));
if ($text === '' || mb_strlen($text) > 3500) { http_response_code(400); echo '{"ok":false}'; exit; }
$text .= "\nСтраница: " . substr((string)($d['page'] ?? ''), 0, 200);

$ch = curl_init('https://api.telegram.org/bot' . BOT_TOKEN . '/sendMessage');
curl_setopt_array($ch, [
  CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8,
  CURLOPT_POSTFIELDS => ['chat_id' => CHAT_ID, 'text' => $text, 'disable_web_page_preview' => 1],
]);
$res = curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);
if ($code === 200) { echo '{"ok":true}'; } else { http_response_code(502); echo '{"ok":false}'; }
