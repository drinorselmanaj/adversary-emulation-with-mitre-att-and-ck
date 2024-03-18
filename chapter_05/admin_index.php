} elseif ($page == 'change_theme') {
if (isset($_POST['send']) && $_POST['send'] == 'send') {
$theme = Validate::validate($_POST['theme'], 'theme'); try {
             Admins::getLocal($userinfo, [
                 'id' => $userinfo['adminid'],
                 'theme' => $theme
])->update();
} catch (Exception $e) {
             Response::dynamicError($e->getMessage());
         }
         $log->logAction(FroxlorLogger::ADM_ACTION, LOG_NOTICE, "changed his/her
    theme to '" . $theme . "'");
         Response::redirectTo($filename);
