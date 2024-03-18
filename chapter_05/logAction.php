public function logAction($action = FroxlorLogger::USR_ACTION, $type = LOG_NOTICE, $text = null)
{
            // not logging normal stuff if not set to "paranoid" logging
if (!self::$crondebug_flag && Settings::Get('logger.severity') == '1' && $type > LOG_NOTICE) {
return; }
if (empty(self::$ml)) { $this->initMonolog();
}
if (self::$crondebug_flag || ($action == FroxlorLogger::CRON_ACTION && $type <= LOG_WARNING)) {
echo "[" . $this->getLogLevelDesc($type) . "] " . $text . PHP_EOL; }
            // warnings, errors and critical messages WILL be logged
if (Settings::Get('logger.log_cron') == '0' && $action == FroxlorLog ger::CRON_ACTION && $type > LOG_WARNING) {
return; }
            $logExtra = [
         'source' => $this->getActionTypeDesc($action),
         'action' => $action,
         'user' => self::$userinfo['loginname']
];
switch ($type) { case LOG_DEBUG:
             self::$ml->addDebug($text, $logExtra);
break; case LOG_INFO:
             self::$ml->addInfo($text, $logExtra);
break;
case LOG_NOTICE:
             self::$ml->addNotice($text, $logExtra);
break;
case LOG_WARNING:
             self::$ml->addWarning($text, $logExtra);
break; case LOG_ERR:
             self::$ml->addError($text, $logExtra);
break; default:
             self::$ml->addDebug($text, $logExtra);
            }
}

