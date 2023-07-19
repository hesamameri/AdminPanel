<?php
    use Silex\Application;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpFoundation\Session\Session;
    use Hashids\Hashids;

    // Shops Customer List
    $app->match("/customer/{page}", function($page) use($app){
        $STEP= 10;
        $sess = new Session();

        $vendor = get_vendorcode();

        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        if(strlen($vendor) == 0){
            $sess->getFlashBag()->add('error', "کد مشتری به کاربر شما اختصاص داده نشده است، با واحد قراردادها تماس حاصل نمایید.");
            return $app->redirect('/');
        }

        $db = DB::getConnection();
        // لیست مشتریان
        $search = "";
        if(!isset($_GET['search'])){            
            $page_sql = ($page+0) * $STEP;
            $row = $db->query("Select a.*, b.title city_name, c.title province_name
                                from customer_sva a
                                left join obj_item b on a.city_id = b.obj_item_id
                                left join obj_item c on a.province_id = c.obj_item_id
                                Where a.reagent = {$vendor}
                                Order By a.obj_item_id desc
                                Limit  {$page_sql},{$STEP}
            ");
        }else{
            $search = strReplace($_GET['search']);

            $row = $db->query("Select a.*, b.title city_name, c.title province_name
                                from customer_sva a
                                left join obj_item b on a.city_id = b.obj_item_id
                                left join obj_item c on a.province_id = c.obj_item_id
                                Where a.reagent = {$vendor}
                                    and (
                                        a.title like '%$search%'
                                        or b.title like '%$search%'
                                        or seller_buyer_id like '%$search%'
                                        or a.obj_item_id like '%$search%'
                                        or codemeli like '%$search%'
                                        or phone like '%$search%'
                                        or mobile like '%$search%'
                                    )
                                Order By a.obj_item_id desc
            ");
        }
            
        // Calc Total Pages
        $rowCount = $db->query("Select count(*) as cnt
                                    from customer_sva a
                                    Where a.reagent = {$vendor}
                                    ")[0];
        $total_page = ceil($rowCount[cnt] / 10);
        $page_next  = $page + 1 <= $total_page ? $page + 1 : -1;
        $page_prior = $page - 1 >= 0 ? $page - 1 : -1;

        // Select for show user column
        $obj_id = 10301;
        $db = DB::getConnection();
        $obj = $db->query("Select a.title obj_type_title, b.title obj_title
                            From obj_type a 
                            join obj b on a.obj_type_id = b.obj_type_id
                            Where b.obj_id = {$obj_id}")[0];

        $obj_spec = $db->query("Select a.*
                                From obj_spec a
                                Where a.obj_id = {$obj_id}
                                order by order_id, obj_spec_id");

        $contract_items = $db->query("Select ci.obj_item_id, p.title as name, p.unit_price
                                        from contract c
                                        join contract_item ci on c.contract_id = ci.contract_id
                                        join product_sva p on ci.obj_item_id = p.obj_item_id
                                        Where c.vendor = {$vendor}
                                              and c.stop_dt is null
                                              and c.sign_dt is not null
                                              and c.type = 'SELL'
                                        ");
        return $app['twig']->render('admin/customer/index.twig', array(
                                                                    'row'=>$row,
                                                                    'contract_id'     => get_last_contracts(),
                                                                    'obj_id'          => $obj_id,
                                                                    'contract_items'  => $contract_items,
                                                                    'tblObj'          => $obj,
                                                                    'tblObjSpec'      => $obj_spec,
                                                                    'total_page'      => $total_page,
                                                                    'page'            => $page,
                                                                    'page_next'       => $page_next,
                                                                    'page_prior'      => $page_prior,
                                                                    'search'          => $search,
                                                                    'form_call'       => 'shop'
                                                                ));
    })->bind('customer.index')->assert('page', '\d+')->value('page', 0);

    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // [x] لیست مشتریان
    $app->get("/customer/all/{page}/{shop_id}", function($page, $shop_id) use($app){
        $STEP= 10; 

        $db = DB::getConnection();
        // لیست مشتریان

        $search = "";
        if(!isset($_GET['search'])){
            $page_sql = ($page+0) * $STEP;
            
            $where = "";
            if($shop_id != -1){
                $where = "And a.reagent = {$shop_id}";
            }

            $row = $db->query("Select a.*, b.title city_name, c.title province_name, shop.title shop_name
                                from customer_sva a
                                left join obj_item b on a.city_id = b.obj_item_id
                                left join obj_item c on a.province_id = c.obj_item_id
                                left join obj_item shop on shop.obj_item_id = a.reagent
                                where length(a.obj_item_id) < 10
                                      {$where}
                                Order By a.obj_item_id DESC
                                Limit  {$page_sql},{$STEP}
                                ");
                                
        }else{
            $search = strReplace($_GET['search']);
            $row = $db->query("Select a.*, b.title city_name, c.title province_name
                                from customer_sva a
                                left join obj_item b on a.city_id = b.obj_item_id
                                left join obj_item c on a.province_id = c.obj_item_id
                                Where (
                                        a.title like '%$search%'
                                        or b.title like '%$search%'
                                        or a.obj_item_id like '%$search%'
                                        or seller_buyer_id like '%$search%'
                                        or codemeli like '%$search%'
                                        or phone like '%$search%'
                                        or mobile like '%$search%'
                                    )
                                    and length(a.obj_item_id) < 10
            ");
        }

        $rowCount   = $db->query("Select count(*) as cnt from customer_sva a")[0];
        $total_page = ceil($rowCount['cnt'] / 10);
        $page_next  = $page + 1 <= $total_page ? $page + 1 : -1;
        $page_prior = $page - 1 >= 0 ? $page - 1 : -1;

        // 
        $row_shop_customer_count = $db->query("Select * from shop_customer_count order by name");


        // سلکت برای نمایش فیلدهای کاربر جدید
        $obj_id = 10301;
        return $app['twig']->render('admin/customer/index-all-customer.twig', 
                                                    array(
                                                            'row'=>$row,
                                                            'contract_id'             => get_last_contracts(),
                                                            'obj_id'                  => $obj_id,
                                                            'total_page'              => $total_page,
                                                            'page'                    => $page,
                                                            'page_next'               => $page_next,
                                                            'page_prior'              => $page_prior,
                                                            'search'                  => $search,
                                                            'shop_id'                 => $shop_id,
                                                            'row_shop_customer_count' => $row_shop_customer_count,
                                                            'form_call' => 'all'
                                                        ));
    })->bind('customer-list.index')->assert('page', '\d+')->assert('shop_id', '\d+')->value('page', 0)->value('shop_id', -1);
    
    //[x] مشتری جدید
    $app->post("/customer/new", function() use($app,$HASH_KEY){

        $sess = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];

        // کد ملی تکراری بودنش برای همین کاربر چک میشود تا کاربر تکراری تعریف ننماید
        // صحت سنجی کد ملی
        $db = DB::getConnection();

        $obj_id = 10301;
        $obj = $db->query("Select a.title obj_type_title, b.title obj_title
                            From obj_type a 
                            join obj b on a.obj_type_id = b.obj_type_id
                            Where b.obj_id = {$obj_id}")[0];

        if(count($obj) <= 0){
            $sess->getFlashBag()->add('error', "خطا شماره 022: خطای نامشخص در سیستم رخ داده است.");
            return $app->redirect('/customer');
        }
    
        $obj_item = array();
        $obj_item_spec = array();
        foreach ($_POST as $key => $value) {
            if(strlen(strpos($key, 'o__')) == 1){
                $obj_item[substr($key, 3, strlen($key))] = $value;
            }
        }
        $obj_item['name'] = $obj_item['title'];

        // چک صحت کد ملی
        $code_meli = $_POST['ois__N8d'];
        if(!check_national_code($code_meli) && $code_meli != '1400'){
            $sess->getFlashBag()->add('error', "کد ملی وارد شده صحیح نمی‌باشد.");
            return $app->redirect('/customer');    
        }
        
        // چک تکراری نبودن کد ملی و شماره موبایل
        $check_1 = $db->query("Select count(*) as cnt
                                From customer_sva
                                Where reagent = {$vendor} and codemeli = '{$code_meli}'
                                ")[0];
        if($check_1['cnt']>0 && $code_meli != '1400'){
            $sess->getFlashBag()->add('error', "کد ملی تکراری می‌باشد، قبلا مشتری با کد ملی فوق ثبت کرده‌اید.");
            return $app->redirect('/customer');
        }

        $mobile  = $_POST['ois__Xm6'];
        $check_1 = $db->query("Select count(*) as cnt, group_concat(name) as name
                                From customer_sva
                                Where reagent = {$vendor} and 
                                        (mobile = '{$mobile}' or mobile = '0{$mobile}')
                                ")[0];
        if($check_1['cnt']>0){
            $name = $check_1['name'];
            $sess->getFlashBag()->add('error', "موبایل وارد شده تکراری است، قبلا برای {$name} ثبت گردیده است.");
        }

        if(count($obj_item)){
            $db = DB::getConnection();
            $obj_item['obj_id'] = $obj_id;
            $insert_id = $db->insert('obj_item', $obj_item);
            
            // ارسال پیامک ثبت نام در پنل تهران الکتریک
            $mobile_number = $_POST['ois__Xm6'];
            if(check_mobile($mobile_number)){
                if(isset($_POST['ois__a9Y'])){
                    $sex_type = $_POST['ois__a9Y'];
                    $sex_type = $db->query("Select ifnull(max(title),'') as title from obj_item where obj_item_id = {$sex_type}")[0]['title'];
                }
                $sess = new Session();
                
                $name         = $_POST['o__title'];
                $smsname      = $sess->get('auth')[0]['smsname'];
                $brand_name   = $sess->get('auth')[0]['brand_name'];
                $brand_slung  = $sess->get('auth')[0]['brand_slung'];
                
                $message = sprintf("خریدار محترم %s ؛ ورود شما را به جمع باشگاه مشتریان%s خیر مقدم عرض می کنیم.\n %s", $name, $brand_name, $brand_slung);
                send_sms($mobile_number, $message);
            }

            $hashids = new Hashids($HASH_KEY); // no padding
            
            foreach ($_POST as $key => $value) {
                if(strlen(strpos($key, 'ois__')) == 1){
                    $obj_item_spec[] = array(
                        'obj_spec_id' => $hashids->decode(substr($key, 5, strlen($key)))[0],
                        'obj_item_id' => $insert_id,
                        'val' => $value
                    );
                }
            }

            $reagentRow = $db->query("Select a.* 
                                    from obj_spec a
                                    join obj_item b on a.obj_id = b.obj_id
                                    where b.obj_item_id = {$insert_id} and a.name = 'reagent'")[0];
            $reagent = $reagentRow['obj_spec_id'];

            $sess = new Session();
            $vendor = $sess->get('auth')[0]['vendor_code'];

            $obj_item_spec[] = array(
                'obj_spec_id' => $reagent,
                'obj_item_id' => $insert_id,
                'val' => $vendor
            );

            // دریافت کد مشتری فروشنده
            $seller_buyer = $db->query("Select a.obj_spec_id, getNextCustomSeq('seller_buyer_id', '{$vendor}') seller_buyer_id
                                                from obj_spec a
                                                Join obj b on a.obj_id = b.obj_id and b.obj_id = 10301
                                                Where a.name = 'seller_buyer_id'")[0];
            $seller_buyer_id = $seller_buyer['obj_spec_id'];
            $seller_buyer_id_val = $seller_buyer['seller_buyer_id'];
            $obj_item_spec[] = array(
                'obj_spec_id' => $seller_buyer_id,
                'obj_item_id' => $insert_id,
                'val' => $seller_buyer_id_val
            );

            // Check Security for add bad code and report to security log
            if(count($obj_item_spec)){
                $db = DB::getConnection();
                $db->insertArray('obj_item_spec', $obj_item_spec);
            }
            $sess->getFlashBag()->add('sccess', "ثبت با موفقیت انجام پذیرفت");
        }else{
            $sess->getFlashBag()->add('error', "خطایی در ارسال اطلاعات رخ داده است");
        }
        return $app->redirect('/customer');
    })->bind('customer.create');
    
    $app->get("/customer/payment/show/{customer_id}", function($customer_id) use($app,$HASH_KEY){
        $hashid = new Hashids($HASH_KEY);
        $customer_id = $hashid->decode($customer_id)[0];

        $db = DB::getConnection();
        $row = $db->query("Select op.*, oi.name customer_name, bank.name bank_name, u.name register_name, oireagent.name reagent_name, odoc.*
                            From obj_payment op
                            join obj_item oi on op.obj_item_id = oi.obj_item_id
                            left join obj_item bank on bank.obj_item_id = op.bank_id
                            left join customer_sva csva on csva.obj_item_id = op.obj_item_id
                            left join obj_item oireagent on oireagent.obj_item_id = csva.reagent
                            join user u on u.user_id = op.register
                            left join obj_document odoc on op.obj_payment_id = odoc.source_id and odoc.source_type = 'CUSTOMER_PAYMENT'
                            Where op.obj_item_id = {$customer_id}
                            Order by op.reg_dt
                            ");

        return $app['twig']->render('admin/customer/customer.payment.confirm.twig', array(
                                                                    'row'=>$row,
                                                                    'hide' => true
                                                                ));
    })->bind('customer.payment.index');

    $app->post("/customer/payment/new", function() use($app,$HASH_KEY){
        $hashid = new Hashids($HASH_KEY);
        $sess = new Session();

        $_POST['obj_item_id'] = $hashid->decode($_POST['buyer_id'])[0];
        unset($_POST['buyer_id']);
        $_POST['source_type'] = 'CUSTOMER_PAYMENT';
        $_POST['source_id']   = $_POST['obj_item_id'] * 1;
        $_POST['register']    = get_userid();
        $_POST['reg_dt']      = get_curdate();
        
        if($_POST['type'] == 'CASH' || $_POST['type'] == 'REBATE'){
            unset($_POST['bank_id']);
            unset($_POST['no']);
            unset($_POST['bank_code']);
            unset($_POST['branch_name']);
            unset($_POST['owner']);
            unset($_POST['branch_code']);
        }

        $db = DB::getConnection();
        $obj_payment_id = $db->insert('obj_payment', $_POST);

        if($_FILES['image']['name'] == ''){
            $sess->getFlashBag()->add('sccess', "پرداختی ثبت گردید، پس از تایید واحد مالی در حساب مشتری لحاظ خواهد گردید.");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $obj_payment_id_encod = $hashid->encode($obj_payment_id);
        
        $obj_document = array(
            'source_type'   => 'CUSTOMER_PAYMENT',
            'source_id'     => $obj_payment_id,
            'document_type' => 'PAYMENT',
            'uri'           => 'nothing.jpg',
            'description'   => '-',
            'hash'          => '-',
        );
        $obj_document_id = $db->insert('obj_document', $obj_document);
        
        $_ext  = pathinfo($_FILES['image']['name'])['extension'];
        $_src  = $_FILES['image']['tmp_name'];
        $_dest = "./uploads/sales/obj_document_{$obj_payment_id}.{$_ext}";
        $_dest_enc = "payment_{$obj_payment_id_encod}.{$_ext}";

        if(!@copy($_src, $_dest)){
        //     // $errors= error_get_last();
        //     // print_r($errors);
        //     // return '---';
        }
        $hash = md5( file_get_contents($_dest) );

        $db->update('obj_document', 
                            array(
                                    'uri' => $_dest_enc,
                                    'hash' => $hash
                            ), 
                            array('obj_document_id' => $obj_document_id));
        $sess->getFlashBag()->add('sccess', "پرداختی ثبت گردید، پس از تایید واحد مالی در حساب مشتری لحاظ خواهد گردید.");
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.payment.new');

    $app->get("/customer/payment/confirm", function() use($app,$HASH_KEY){
        $db = DB::getConnection();
        $row = $db->query("Select op.*, oi.name customer_name, bank.name bank_name, u.name register_name, oireagent.name reagent_name, odoc.*
                            From obj_payment op
                            join obj_item oi on op.obj_item_id = oi.obj_item_id
                            left join obj_item bank on bank.obj_item_id = op.bank_id
                            left join customer_sva csva on csva.obj_item_id = op.obj_item_id
                            left join obj_item oireagent on oireagent.obj_item_id = csva.reagent
                            join user u on u.user_id = op.register
                            left join obj_document odoc on op.obj_payment_id = odoc.source_id and odoc.source_type = 'CUSTOMER_PAYMENT'
                            Where op.confirm_status is null
                                or (op.confirm_status is null is not null and doc_register_id is null)
                            
                            ");
        return $app['twig']->render('admin/customer/customer.payment.confirms.twig', array('row'=>$row,));
    })->bind('customer.payment.confirm');

    $app->get("/customer/payment/doc/register", function() use($app,$HASH_KEY){
        $db = DB::getConnection();
        $row = $db->query("Select op.*, oi.name customer_name, bank.name bank_name, u.name register_name, oireagent.name reagent_name, odoc.*
                            From obj_payment op
                            join obj_item oi on op.obj_item_id = oi.obj_item_id
                            left join obj_item bank on bank.obj_item_id = op.bank_id
                            left join customer_sva csva on csva.obj_item_id = op.obj_item_id
                            left join obj_item oireagent on oireagent.obj_item_id = csva.reagent
                            join user u on u.user_id = op.register
                            left join obj_document odoc on op.obj_payment_id = odoc.source_id and odoc.source_type = 'CUSTOMER_PAYMENT'
                            Where op.confirm_status is null
                                or (op.confirm_status is null is not null and doc_register_id is null)
                            
                            ");
        return $app['twig']->render('admin/customer/customer.payment.confirms.twig', array(
                                                                    'row'=>$row,
                                                                ));
    })->bind('customer.payment.doc.register');

    $app->post("/customer/payment/confirm", function() use($app,$HASH_KEY){
        $obj_payment_id = $_POST['payment_id'];

        if($_POST['price'] * 1 <= 0){
            unset($_POST['price']);
        }

        $_POST['confirmer']    = get_userid();
        $_POST['confirm_dt']   = get_curdate();

        unset($_POST['payment_id']);

        $db = DB::getConnection();
        $db->update('obj_payment', $_POST, array('obj_payment_id' => $obj_payment_id));
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.payment.confirm.post');

    $app->post("/customer/payment/doc-register", function() use($app,$HASH_KEY){
        $obj_payment_id = $_POST['payment_id'];

        if($_POST['price'] * 1 <= 0){
            unset($_POST['price']);
        }

        $_POST['doc_register_id']     = get_userid();
        $_POST['doc_register_dt']     = get_curdate();
        $_POST['roc_register_desc']   = $_POST['confirm_desc'];

        
        unset($_POST['payment_id']);
        unset($_POST['confirm_desc']);

        $db = DB::getConnection();
        $db->update('obj_payment', $_POST, array('obj_payment_id' => $obj_payment_id));
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.payment.doc.post');

    //[X] استعلام جدید
    $app->post("/customer/inquiry/new", function() use($app,$HASH_KEY){
        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];

        if(mb_strlen($_POST['bank_branch']) <= 0){
            $sess->getFlashBag()->add('error', "نام شعبه وارد نشده است");
            return $app->redirect('/customer');
        }
        if(!isInteger($_POST['bank_code'])){
            $sess->getFlashBag()->add('error', "کد شعبه عدد باید باشد");
            return $app->redirect('/customer');
        }
        if($_POST['bank_code']*1 <= 0){
            $sess->getFlashBag()->add('error', "کد شعبه بانک را وارد نمایید");
            return $app->redirect('/customer');
        }
        if(!isInteger($_POST['account_sayadi'])){
            $sess->getFlashBag()->add('error', "شماره صیادی شامل فقط عدد باشد");
            return $app->redirect('/customer');
        }
        if(strlen($_POST['account_sayadi']) <> 16){
            $sess->getFlashBag()->add('error', "شماره صیادی 16 رقم باید باشد");
            return $app->redirect('/customer');
        }

        if(!isInteger($_POST['cheque_price'])){
            $sess->getFlashBag()->add('error', "مبلغ چک صحییح وارد نشده است");
            return $app->redirect('/customer');
        }
        if(!isInteger($_POST['cheque_count'])){
            $sess->getFlashBag()->add('error', "تعداد چک صحییح وارد نشده است");
            return $app->redirect('/customer');
        }

        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $_POST['buyer_id'];
        $_POST['buyer_id'] = $hashids->decode($customer_id_encoded)[0];

        $buyer_id = $_POST['buyer_id']*1;
        $db = DB::getConnection();
        $check_1 = $db->query("Select count(*) as cnt
                                From customer_sva
                                Where reagent = {$vendor_id} and obj_item_id = $buyer_id
                                ")[0];
        if($check_1['cnt'] <= 0){
            // Hack
            $sess->getFlashBag()->add('error', "خطای سیستمی در شناسایی مشتری، مجدد سعی نمایید.");
            return $app->redirect('/customer');
            // Check cusomer_id created with loggined user
        }

        // send_sms
        $check_1 = $db->query("Select *
                                From customer_sva
                                Where obj_item_id = $buyer_id
                                ")[0];
        $mobile_number = $check_1['mobile'];
        $name          = $check_1['title'];
        $sex_type      = $check_1['sex_title'];
        $brand_name    = $check_1['brand_name'];
        $brand_slung   = $check_1['brand_slung'];
        if(check_mobile($mobile_number)){
            $message = sprintf("%s %s \n استعلام حساب شما جهت بررسی در سامانه مالی %s ثبت گردید.\n%s", $sex_type, $name, $brand_name, $brand_slung);
            send_sms($mobile_number, $message);
        }

        $sess = new Session();
        $_POST['register'] = get_userid();
        $db->insert('inquiry', $_POST);

        $sess->getFlashBag()->add('info', "ثبت استعلام با موفقیت صورت پذیرفت.");
        return $app->redirect('/customer');
    })->bind('customer.inquiry.new');

    // [x] لیست فاکتورهای هر فروشگاه که اقدامی برای آن ها صورت نپذیرفته است
    $app->get("/customer/preforma", function() use($app,$HASH_KEY){
        $sess = new Session();
        $vendor_code = get_vendorcode();

        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        if(strlen($vendor_code) == 0){
            $sess->getFlashBag()->add('error', "کد مشتری به کاربر شما اختصاص داده نشده است، با واحد قراردادها تماس حاصل نمایید.");
            return $app->redirect('/');
        }

        $db = DB::getConnection();
        // لیست فاکتورهایی که هنوز ثبت نشده اند
        $row = $db->query("Select a.*, b.seller_buyer_id, b.title buer_name
                            From factor a
                            join customer_sva b on a.buyer_id = b.obj_item_id
                            join contract c on  a.contract_id = c.contract_id 
                                                and c.vendor = {$vendor_code}
                                                and a.reg_status is null
                            Where a.register is null
                            ");
        return $app['twig']->render('admin/customer/prefroma.twig', array(
                                                                    'row'=>$row,
                                                                ));
    })->bind('customer.preforma');
    
    // [X] رد فاکتور توسط فروشگاه
    $app->match("/customer/{customer_id}/factor/{factor_id}/reject", function($customer_id,$factor_id) use($app,$HASH_KEY){
        $hashids     = new Hashids($HASH_KEY);
        $customer_id = $hashids->decode($customer_id)[0];
        $factor_id   = $hashids->decode($factor_id)[0];

        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];

        $db = DB::getConnection();

        // [x] چک شودمشتری برای خود فروشنده باشد
        $check_1 = $db->query("Select count(*) as cnt
                                From customer_sva
                                Where reagent = {$vendor_id} and obj_item_id = $customer_id
                                ")[0];
        if($check_1['cnt'] <= 0){
            // Hack
            $sess->getFlashBag()->add('error', "خطای سیستمی در شناسایی مشتری، مجدد سعی نمایید.");
            return $app->redirect('/customer/preforma');
            // Check cusomer_id created with loggined user
        }
        // [ ] چک شود فاکتور قبلا تایید یا رد نشده باشد
        $check_1 = $db->query("Select count(*) as cnt
                                From factor
                                Where factor_id = {$factor_id}
                                    and reg_status is NULL
                                ")[0];
        if($check_1['cnt'] <= 0){
            // Hack
            $sess->getFlashBag()->add('error', "فاکتور فوق متعلق به شما نمی باشد.");
            return $app->redirect('/customer/preforma');
            // Check cusomer_id created with loggined user
        }

        $db->update('factor', array(
                                'reg_status' => 'REJECT',
                                'reg_dt' => curdate(),
                                'register' => get_userid(),
                            ), array('factor_id'=>$factor_id));

        return $app->redirect('/customer/preforma');
    })->bind('customer.factor.reject');

    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // [x] درخواست فاکتور جدید و دریافت شماره فاکتور
    $app->get("/customer/{customer_id}/factor/new", function($customer_id) use($app,$HASH_KEY){
        $hashids  = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id)[0];
    
        $insert_array = array();
        $sess = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];
        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        if(strlen($vendor) == 0){
            return $app->redirect('/');
        }
    
        $db = DB::getConnection();
        // اگر مشتری وارد سیستم شده قرارداد فعال نداشته باشد به صفحه اصلی هدایت خواهد شد
        // تصویب شده باشد و متوقف نشده باشد
        // تاریخ قرارداد فعلا چک نمی‌شود
        $contract = $db->query("Select * from contract where type = 'SELL' and vendor = {$vendor} and sign_dt is not null and stop_dt is null")[0];
        if(count($contract) == 0){
            $sess->getFlashBag()->add('error', "در سیستم قرارداد فعال پیدا نشد. با واحد قراردادها تماس بگیرید.");
            return $app->redirect('/customer');
        }
        $insert_array['contract_id'] = $contract['contract_id'];
    
        //[ ] چک شود قرارداد مانده داشته باشد
            
        // اگر خریدار ثبت فاکتور شده متعلق به کاربر فوق نمی باشد
        // برای مشتری که غیر فعال شده است نمی توان فاکتور صادر نمود        
        $customer  = $db->query("Select * from customer_sva where obj_item_id = {$customer_id} and status = 1 and reagent = {$vendor}")[0];
        if(count($customer) == 0){
            $sess->getFlashBag()->add('error', "مشتری فوق در سیستم فعال نمی‌باشد.");
            return $app->redirect('/customer');
        }
        $insert_array['buyer_id'] = $customer_id;
    
        $factor_id = $db->insert('factor', $insert_array);
    
        $address = $db->query("Select title receiver, phone, mobile, city_id, address, {$factor_id} factor_id from customer_sva where obj_item_id = {$customer_id}")[0];
        $db->insert('factor_address', $address);

        $hashids = new Hashids($HASH_KEY);
        $factor_id = $hashids->encode($factor_id);

        $db->update('inquiry', array('shower'=>get_userid(), 'show_dt'=>curdate()), array('buyer_id' => $customer_id));

        return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
    })->bind('customer.factor.new');

    // [X] فرم فاکتور
    $app->get("/customer/{customer_id}/factor/{factor_id}/{_type}", function($customer_id, $factor_id, $_type) use($app,$HASH_KEY){
        $hashids             = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id         = $hashids->decode($customer_id_encoded)[0];

        $hashid    = new Hashids($HASH_KEY);
        $factor_id = $hashid->decode($factor_id)[0];

        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        $sess   = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];

        $sess->set('_factor_call_type', $_type);
        if(strlen($vendor) == 0 && $_type == 'customer'){
            $sess->getFlashBag()->add('error', "کد مشتری برای شما اختصاص داده نشده است. با امور قراردادها تماس گرفته شود.");
            return $app->redirect('/');
        }

        $db = DB::getConnection();

        $factor_check_confirmed = true;
        $row_check_1 = $db->query("SELECT Count(*) as cnt
                                    FROM factor_inquiry_sva a
                                    Where a.factor_id = {$factor_id}
                                            and inquiry_status_sign = 1")[0];
        if($row_check_1['cnt'] == 0){
            $factor_check_confirmed = false;
        }

        // اگر مشتری وارد سیستم شده قرارداد فعال نداشته باشد به صفحه اصلی هدایت خواهد شد
        // تصویب شده باشد و متوقف نشده باشد
        // تاریخ قرارداد فعلا چک نمی‌شود

        if($_type == 'show'){
            $contract = $db->query("Select * from contract where type = 'SELL' and vendor = {$vendor} and sign_dt is not null and stop_dt is null")[0];
            if(count($contract) == 0){
                $sess->getFlashBag()->add('error', "قرارداد شما فعال نشده است. با امور قراردادها تماس گرفته شود.");
                return $app->redirect('/customer');
            }

            // اگر خریدار ثبت فاکتور شده متعلق به کاربر فوق نمی باشد
            // برای مشتری که غیر فعال شده است نمی توان فاکتور صادر نمود        
            $customer  = $db->query("Select * from customer_sva where obj_item_id = {$customer_id} and status = 1 and reagent = {$vendor}")[0];
            if(count($customer) == 0 && $_type == 'customer'){
                $sess->getFlashBag()->add('error', "مشتری فوق غیرفعال شده است");
                return $app->redirect('/customer');
            }
            $insert_array['buyer_id'] = $customer_id;

            $factor = $db->query("Select a.*, b.*, c.title city_name
                                        , a.city_id factor_city_id
                                        , a.phone   factor_phone
                                        , a.mobile  factor_mobile
                                        , a.receiver factor_receiver
                                        , a.address  factor_address
                                        , d.title factor_city_name
                                    from factor a
                                    join customer_sva b on a.buyer_id = b.obj_item_id
                                    left join obj_item c on b.city_id = c.obj_item_id
                                    left join obj_item d on a.city_id = d.obj_item_id
                                    where a.factor_id = {$factor_id}
                                    ")[0];
        }elseif($_type == 'customer'){
            $contract = $db->query("Select * from contract where type = 'SELL' and vendor = {$vendor} and sign_dt is not null and stop_dt is null")[0];
            if(count($contract) == 0){
                $sess->getFlashBag()->add('error', "قرارداد شما فعال نشده است. با امور قراردادها تماس گرفته شود.");
                return $app->redirect('/customer');
            }
            $insert_array['contract_id'] = $contract['contract_id'];

            // اگر خریدار ثبت فاکتور شده متعلق به کاربر فوق نمی باشد
            // برای مشتری که غیر فعال شده است نمی توان فاکتور صادر نمود        
            $customer  = $db->query("Select * from customer_sva where obj_item_id = {$customer_id} and status = 1 and reagent = {$vendor}")[0];
            if(count($customer) == 0 && $_type == 'customer'){
                $sess->getFlashBag()->add('error', "مشتری فوق غیرفعال شده است");
                return $app->redirect('/customer');
            }
            $insert_array['buyer_id'] = $customer_id;

            // اگر فاکتور ثبت شده است امکان ویرایش وجود نداشته باشد
            // به صفحه لیست فاکتورهای پیش نویس منتقل شود
            $factor = $db->query("Select a.*, b.*, c.title city_name
                                        , a.city_id factor_city_id
                                        , a.phone   factor_phone
                                        , a.mobile  factor_mobile
                                        , a.receiver factor_receiver
                                        , a.address  factor_address
                                    from factor a
                                    join customer_sva b on a.buyer_id = b.obj_item_id
                                    left join obj_item c on b.city_id = c.obj_item_id
                                    where a.factor_id = {$factor_id} and a.register is null and a.reg_status is null")[0];
        }elseif($_type == 'account'){
            // [x]todo: اگر فاکتور دارای استعلام تایید شده است اطلاعات نمایش داده شوند
            $row_check_1 = $db->query("SELECT Count(*) as cnt
                                            FROM factor_inquiry_sva a
                                            Where a.factor_id = {$factor_id}
                                            group by factor_id
                                            having count(*) = sum(a.inquiry_status_sign)")[0];
            if($row_check_1['cnt'] == 0){
                // return $app->redirect('/');
            }

            $factor = $db->query("Select a.*, b.*, c.title city_name
                                        , a.city_id  factor_city_id
                                        , a.phone    factor_phone
                                        , a.mobile   factor_mobile
                                        , a.receiver factor_receiver
                                        , a.address  factor_address
                                        , d.title    factor_city_name
                                    from factor a
                                    join customer_sva b on a.buyer_id = b.obj_item_id
                                    left join obj_item c on b.city_id = c.obj_item_id
                                    left join obj_item d on a.city_id = d.obj_item_id
                                    where a.factor_id = {$factor_id} and a.register is not null and acc_confirmer is null")[0];    
        }elseif($_type == 'sale'){
            $factor = $db->query("Select a.*, b.*, c.title city_name
                                        , a.city_id factor_city_id
                                        , a.phone   factor_phone
                                        , a.mobile  factor_mobile
                                        , a.receiver factor_receiver
                                        , a.address  factor_address
                                        , d.title factor_city_name
                                    from factor a
                                    join customer_sva b on a.buyer_id = b.obj_item_id
                                    left join obj_item c on b.city_id = c.obj_item_id
                                    left join obj_item d on a.city_id = d.obj_item_id
                                    where a.factor_id = {$factor_id}
                                        and a.register is not null
                                        and a.acc_confirmer is not null
                                        and a.acc_status = 1
                                        and a.sale_confirmer is null")[0];
        }

        if(count($factor) == 0 && $_type == 'customer'){
            return $app->redirect('/customer');
        }
        if(count($factor) == 0 && $_type == 'show'){
            return $app->redirect('/customer');
        }

        // اگر کاربر غیر فعال شده باشد امکان ادامه فاکتور فوق فراهم نخواهد بود
        if($factor['status'] == 0 && $_type == 'customer'){
            return $app->redirect('/customer');
        }
        if($factor['status'] == 0 && $_type == 'show'){
            return $app->redirect('/customer');
        }

        // لیست استعلام‌های گرفته شده برای مشتری
        $inquiry = $db->query("Select a.*, b.title bank_name,
                                case 
                                    when a.confirm_status = 'CONFIRM' Then 'تایید'
                                    when a.confirm_status = 'COND_CONFIRM' Then 'تایید مشروط'
                                    when a.confirm_status = 'REJECT' Then 'رد'
                                end confirm_status_name
                                from inquiry a
                                left join obj_item b on a.bank_id = b.obj_item_id
                                where a.buyer_id = {$customer_id}");
        
        // لیست محصولات موجود در قرارداد و دارای مانده
        // مانده قرارداد باید چک شود و بر اساس مانده از قرارداد امکان فروش فراهم باشد
        $product_list = $db->query("Select c.*, d.name, d.title, d.unit_price product_unit_price
                                        from factor a
                                        join contract b on a.contract_id = b.contract_id
                                        join contract cont on b.vendor = cont.vendor and cont.confirmer is not null and cont.signer is not null and cont.stoper is null
                                        join contract_item c on cont.contract_id = c.contract_id
                                        join product_sva d on c.obj_item_id = d.obj_item_id
                                        Where   a.factor_id = {$factor_id}
                                                -- and b.vendor = {$vendor}
                                    ");
        
        // لیست آیتم های اضافه شده به قرارداد
        $factor_item = $db->query("Select   a.factor_item_id, a.factor_id, a.obj_item_id, a.amount, a.unit_price, a.price, a.discount_percent, a.discount_price, a.related_factor_item_id, a.register, a.reg_dt, a.depo_id
                                            , b.name, b.title, b.status product_status
                                            , round(a.discount_price + ((a.price * a.discount_percent) / 100)) as price_discount
                                            , ifnull(sum(c.fixed_rate),0) + round((1+ifnull(sum(c.percent_rate), 0)/100)*(a.price - round(a.discount_price + ((a.price * a.discount_percent) / 100)))) as price_kol
                                            , ifnull(sum(c.fixed_rate),0) + round((ifnull(sum(c.percent_rate), 0)/100)*(a.price - round(a.discount_price + ((a.price * a.discount_percent) / 100)))) as price_organ
                                            , (1+ifnull(sum(c.percent_rate), 0)/100) organ_percent_rate
                                            , ifnull(sum(c.fixed_rate),0) organ_fixed_rate
                                    from factor_item a
                                    join obj_item b on a.obj_item_id = b.obj_item_id
                                    left join factor_item_organ c on a.factor_item_id = c.factor_item_id
                                    where a.factor_id = {$factor_id}
                                    Group by a.factor_item_id, a.factor_id, a.obj_item_id, a.amount, a.unit_price, a.price, a.discount_percent, a.discount_price, a.related_factor_item_id, a.register, a.reg_dt
                                            , b.name, b.title, b.status, a.depo_id
                                    ");

        // اطلاعات پرداختی های فاکتور
        $factor_payway = $db->query("Select a.*,
                                        b.title bank_name,
                                        u.name register_name,
                                        (Select count(*) from factor_payway b where b.no = a.no) repeated,
                                        (Select group_concat(factor_id) from factor_payway b where b.no = a.no) repeated_factor_id
                                    From factor_payway a
                                    left join obj_item b on a.bank_id = b.obj_item_id
                                    left join user u on u.user_id = a.register
                                    Where a.factor_id = {$factor_id}
                                        -- And pay_level = 'FACTOR'
                                    ");

        $factor_payway_rebate = $db->query("Select ifnull(sum(price),0) as rebate_price
                                    From factor_payway a
                                    left join obj_item b on a.bank_id = b.obj_item_id
                                    Where a.factor_id = {$factor_id}
                                        And a.pay_type = 'REBATE'
                                    ")[0];
        // تصاویر آپلود شده
        $factor_document = $db->query("Select a.*,
                                            u.name register_name,
                                            (Select count(*) from factor_document b where b.hash = a.hash) repeated,
                                            (Select group_concat(factor_id) from factor_document b where b.hash = a.hash) repeated_factor_id
                                    From factor_document a
                                    left join user u on u.user_id = a.register
                                    Where a.factor_id = {$factor_id}
                                        -- And level_type = 'FACTOR'
                                    ");

        $credit = $db->query("Select credit.* 
                            From factor f
                            join contract cont on f.contract_id = cont.contract_id
                            join credit_sum_sva credit on credit.vendor_buyer_id = cont.vendor
                            Where f.factor_id = {$factor_id}
                            ");

        $factor_address = $db->query("Select a.*, b.title city_name
                                        from factor_address a
                                        join obj_item b on a.city_id = b.obj_item_id
                                        where factor_id = {$factor_id}");

        $depo_send = $db->query("
                        Select ds.*, u.name register_name, oi.name good_name, oi_depo.title depo_name
                            From depo_send ds
                            Join factor_item fi on fi.factor_item_id = ds.source_id and fi.factor_id = {$factor_id}
                            join obj_item oi on oi.obj_item_id = ds.goods
                            join obj_item oi_depo on oi_depo.obj_item_id = ds.depo_id
                            left join user u on ds.register = u.user_id
                            Where ds.source_type = 'FACTOR'
                            ");
        $obj_send = $db->query("
                        Select GROUP_CONCAT(DISTINCT oi.name) good_name, GROUP_CONCAT(DISTINCT oi_depo.title) depo_name
                                , os.obj_send_id, os.action
                                , os.print_id, os.print_dt, os.print_desc
                                , os.drive_id, os.drive_dt, os.drive_desc
                                
                                , os.drive_status, os.drive_status_id, os.drive_status_dt, os.drive_status_desc, drive_register
                                , os.assesmenter,os.assesment_dt,os.assesment_desc,os.assesment_opinion
                                , os.docer,os.doc_dt,os.doc_desc,os.price

                                , u.name print_name
                                , u1.name drive_register_name
                                , oi_driver.title driver_name
                            From depo_send ds
                            Join factor_item fi on fi.factor_item_id = ds.source_id and fi.factor_id = {$factor_id}
                            join obj_send os on os.source_id = ds.depo_send_id and os.action in ('DRIVE', 'INSTALL') and os.source_type = 'FACTOR'
                            join obj_item oi on oi.obj_item_id = ds.goods
                            join obj_item oi_depo on oi_depo.obj_item_id = ds.depo_id
                            join obj_item oi_driver on oi_driver.obj_item_id = os.drive_id
                            left join user u on os.print_id = u.user_id
                            left join user u1 on os.drive_register = u1.user_id
                            Where ds.source_type = 'FACTOR'
                                group by os.action
                                            , os.print_id, os.print_dt, os.print_desc
                                            , os.drive_id, os.drive_dt, os.drive_desc

                                            , os.drive_status, os.drive_status_id, os.drive_status_dt, os.drive_status_desc, drive_register
                                            , os.assesmenter,os.assesment_dt,os.assesment_desc,os.assesment_opinion
                                            , os.docer,os.doc_dt,os.doc_desc,os.price

                                            , u.name
                            Order by os.obj_send_id
                            ");

        $customer_reminded_account = $db->query("Select Sum(Debit) debit,Sum(Credit) credit, Sum(Credit)-Sum(Debit) reminded
                                                    From customer_payment
                                                    Where obj_item_id = {$customer_id}
                                                            and source_type <> '{$factor_id}'
                                                ")[0];

        return $app['twig']->render('admin/customer/factor.twig', array(
            'factor'          => $factor,
            'credit'          => $credit[0],
            'factor_address'  => $factor_address,
            'product_list'    => $product_list,
            'inquiry'         => $inquiry,
            'factor_item'     => $factor_item,
            'customer_id'     => $customer_id,
            'factor_id'       => $factor_id,
            'factor_document' => $factor_document,
            'factor_payway'   => $factor_payway,
            '_type'           => $_type,
            'contract_id'     => get_last_contracts(),
            'depo_send'       => $depo_send,
            'obj_send'        => $obj_send,
            'customer_reminded_account' => $customer_reminded_account,
            'factor_payway_rebate'      => $factor_payway_rebate,
            'factor_check_confirmed'    => $factor_check_confirmed,
        ));
    })->bind('customer.factor.show')->value('_type', 'customer');

    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP
    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP
    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP

    // [ ] ویرایش مشخصات مشتریان قبل از صدور اولین فاکتور
    $app->get("/customer/edit/{customer_id}", function($customer_id) use($app){
    })->bind('customer.edit');
    // [ ] ویرایش مشخصات مشتریان قبل از صدور اولین فاکتور
    $app->post("/customer/edit/{customer_id}", function($customer_id) use($app){
    })->bind('customer.update');

    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP
    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP
    // POPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOPPOP
    // [x] لیست استعلام‌های منتظر تایید مالی
    $app->get("/customer/inquiry", function() use($app){
        $sess = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor) == 0){
            return $app->redirect('/');
        }

        $db = DB::getConnection();
        $row = $db->query("Select   a.*, 
                                    b.title city_name, 
                                    c.title province_name, 
                                    d.*, 
                                    e.title bank_name, 
                                    pdate(d.reg_dt) factor_reg_dt, f.name register_name
                                    , g.title seller_name
                            from customer_sva a
                            left join obj_item b on a.city_id = b.obj_item_id
                            left join obj_item c on a.province_id = c.obj_item_id
                            join inquiry d on a.obj_item_id = d.buyer_id
                            left join obj_item e on d.bank_id = e.obj_item_id
                            left join user f on f.user_id = d.register
                            left join obj_item g on a.reagent = g.obj_item_id
                            Where reg_dt is not null
                                    and confirm_dt is null
                            order by d.reg_dt ASC");

        return $app['twig']->render('admin/customer/index.inquiry.twig', array('row'=>$row));
    })->bind('customer.inquiry.index');
    // [x] ثبت پاسخ استعلام توسط مالی
    $app->post("/customer/inquiry/response", function() use($app){
        $sess = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor) == 0){
            return $app->redirect('/');
        }

        $inquiry_id = $_POST['inquiry_id']*1;
        unset($_POST['inquiry_id']);

        // Check cusomer_id created with loggined user
        $db = DB::getConnection();

        $sess = new Session();
        $_POST['confirmer']  = $sess->get('auth')[0]['user_id'];
        $_POST['confirm_dt'] = curdate();
        $db->update('inquiry', $_POST, array('inquiry_id' => $inquiry_id));

        if($_POST['confirm_status'] == 'REJECT'){
            $factor_list = $db->query("Select DISTINCT f.factor_id
                                        From factor f
                                        Join factor_payway fp on f.factor_id = fp.factor_id
                                        join inquiry i on i.buyer_id = f.buyer_id
                                        Where i.inquiry_id = {$inquiry_id}
                                            and fp.pay_type in ('CHEQUE')
                                            and f.reg_status = 'CONFIRM'", true);
            foreach ($factor_list as $key => $value) {
                $update = array('acc_confirmer' => get_userid(), 'acc_confirm_dt' => curdate(), 'acc_status' => 0, 'acc_description'=>"رد خودکار، پاسخ استعلام {$inquiry_id}");
                $db->update("factor", $update, array('factor_id' => $value['factor_id']));
            }
        }
        // Send SMS Inquery Accept
        $check_1 = $db->query("Select a.*
                                    from inquiry b
                                    left join customer_sva a on b.buyer_id = a.obj_item_id
                                    Where b.inquiry_id = {$inquiry_id}
                                ")[0];
        $mobile_number = $check_1['mobile'];
        $name          = $check_1['title'];
        $reagent_title = $check_1['reagent_title'];
        $sex_type      = $check_1['sex_title'];

        $brand_name    = $check_1['brand_name'];
        $brand_phone   = $check_1['brand_phone'];
        $brand_slung   = $check_1['brand_slung'];
        if(check_mobile($mobile_number)){
            
            if($_POST['confirm_status']=='REJECT'){
                $message = sprintf("مشتری گرامی %s %s \n نتیجه استعلام شماره حساب اعلامی شما مورد تایید نمی باشد در صورت تمایل به ادامه فرآیند خرید دراسرع وقت نسبت به اعلام شماره حساب جدید اقدام نمایید و یا با شماره تلفن %s تماس حاصل فرمائید\n %s", $sex_type, $name, $brand_phone, $brand_slung);
            }else{
                $message = sprintf("مشتری گرامی %s %s \n نتیجه استعلام شماره حساب اعلامی شما مورد تایید می باشد لطفاً نسبت به تحویل اسناد به شعبه مربوطه مراجعه نمائید و یا با شماره تلفن %s تماس حاصل فرمائید\n %s", $sex_type, $name, $brand_phone, $brand_slung);
            }
            send_sms($mobile_number, $message);
        }
        return $app->redirect('/customer/inquiry');
    })->bind('customer.inquiry.response');

    // [x] لیست استعلام‌های پاسخ داده شده به مشتری برای فروشگاه
    $app->get("/customer/inquiry/response", function() use($app){
        $sess = new Session();
        $vendor = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor) == 0){
            return $app->redirect('/');
        }

        $db = DB::getConnection();
        $row = $db->query("Select a.*,  b.title city_name, c.title province_name, d.*, e.title bank_name,
                                    case 
                                        when sms_inquiry = 5 Then 'سبز'
                                        when sms_inquiry = 4 Then 'زرد'
                                        when sms_inquiry = 3 Then 'نارنجی'
                                        when sms_inquiry = 2 Then 'قرمز'
                                        when sms_inquiry = 1 Then 'قهوه‌ای'
                                    end sms_inquiry_name,
                                    case 
                                        when direct_inquiry = 1 Then 'تایید'
                                        when direct_inquiry = 0 Then 'رد'
                                    end direct_inquiry_name,
                                    case 
                                        when confirm_status = 'CONFIRM' Then 'تایید'
                                        when confirm_status = 'COND_CONFIRM' Then 'تایید مشروط'
                                        when confirm_status = 'REJECT' Then 'رد'
                                    end confirm_status_name,
                                    pdate(confirm_dt) confirm_dt
                            from customer_sva a
                            left join obj_item b on a.city_id = b.obj_item_id
                            left join obj_item c on a.province_id = c.obj_item_id
                            join inquiry d on a.obj_item_id = d.buyer_id
                            left join obj_item e on d.bank_id = e.obj_item_id
                            Where   reg_dt is not null 
                                    and confirm_dt is not null 
                                    and action_dt is null
                                    and a.reagent = {$vendor}
                                    and d.show_dt is null
                            order by d.reg_dt ASC");

        return $app['twig']->render('admin/customer/index.inquiry.response.twig', array('row'=>$row));
    })->bind('customer.inquiry.response.show');
    // [x] مشاهده استعلام و خروج از لیست استعلام های فروشگاه
    $app->get("/customer/inquiry/show/{inquiry_id}", function($inquiry_id) use($app,$HASH_KEY){
        $hashids = new Hashids($HASH_KEY);
        $inquiry_id = $hashids->decode($inquiry_id)[0];

        // [ ] چک شود که مشتری برای فروشنده ای باشد که وارد سیستم شده است، هک
        // Select * from inquery a join customer_sva b on a.buyer_id = b.obj_item_id
        
        $sess = new Session();
        $user_id = $sess->get('auth')[0]['vendor_code'];

        $db = DB::getConnection();
        $db->update('inquiry', array('shower'=>$user_id, 'show_dt'=>curdate()), array('inquiry_id' => $inquiry_id));
        return $app->redirect('/customer/inquiry/response');
    })->bind('inquiry.show');

    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // [x] ثبت محصول به فاکتور
    $app->post("/customer/{customer_id}/factor/{factor_id}/product/add", function($customer_id, $factor_id) use($app,$HASH_KEY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id)[0];
                
        $hashid = new Hashids($HASH_KEY);
        $factor_id_decoded = $hashid->decode($factor_id)[0];


        $db = DB::getConnection();
        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        $sess = new Session();

        $_factor_call_type =  $sess->get('_factor_call_type');
        $_factor_call_type_is_customer = $_factor_call_type == 'customer' ? true : false;

        $vendor_id = get_vendorcode();
        if(strlen($vendor_id) == 0 && !$_factor_call_type_is_customer){
            $sess->getFlashBag()->add('error', "کد مشتری به کاربر شما اختصاص داده نشده است، با واحد قراردادها تماس حاصل نمایید.");
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }

        $product_id = $_POST['product_id'] * 1;

        // چک شود کالا در قرارداد کاربر وجود داشته باشد
        // اگر قرارنداشته باشد یعنی کد به صورت اشتباهی ارسال شده است
        $product_list = $db->query("Select c.*, d.name, d.title, d.unit_price product_unit_price
                                        from factor a
                                        join contract b on a.contract_id = b.contract_id
                                        join contract cont on b.vendor = cont.vendor and cont.confirmer is not null and cont.signer is not null and cont.stoper is null
                                        join contract_item c on cont.contract_id = c.contract_id
                                        join product_sva d on c.obj_item_id = d.obj_item_id
                                        Where   a.factor_id = {$factor_id_decoded} 
                                                -- and b.vendor = {$vendor_id} 
                                                and d.product_id = {$product_id}
                                    ")[0];

        if(count($product_list)<=0 && !$_factor_call_type_is_customer){
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $amount = $_POST['amount'] * 1;
        if($amount <= 0){
            $sess->getFlashBag()->add('error', "مقدار وارد شده صحیح نمی‌باشد.");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $insert_arr = array(
            'factor_id'   => $factor_id_decoded,
            'obj_item_id' => $product_id,
            'amount'      => $amount,
            'unit_price'  => $product_list['product_unit_price'],
            // 'price' => $amount * $product_list['product_unit_price'],
            'register'    => $sess->get('auth')[0]['user_id'],
            'reg_dt'      => curdate(),
        );

        // ثبت آیتم
        // اگر آیتم ثبت شده است بروزرسانی فاکتور ثبت شود و اگر آیتم وجود نداشت ثبت شود
        $exist_product = $db->query("Select count(*) as cnt, max(factor_item_id) factor_item_id 
                                        from factor_item
                                        where   related_factor_item_id is null 
                                                and factor_id = {$factor_id_decoded} 
                                                and obj_item_id = {$product_id}")[0];
        $factor_item_id = $exist_product['factor_item_id'];

        if($exist_product['cnt'] > 0){
            $db->exec("update factor_item set amount = amount+{$amount}, unit_price = {$product_list['product_unit_price']} where factor_id = {$factor_id_decoded} and obj_item_id = {$product_id}");
        }else{
            $factor_item_id = $db->insert('factor_item', $insert_arr);
        }

        // ثبت آیتم های افزوده
        $db->query("Delete from factor_item where factor_id = {$factor_id_decoded} and related_factor_item_id is not null");
        $product_additional_row = $db->query("SELECT    {$factor_id_decoded} factor_id,
                                                        c.obj_item_add_id obj_item_id, 
                                                        c.amount*a.amount amount,
                                                        {$sess->get('auth')[0]['user_id']} register, 
                                                        '".date('Y-m-d H:i:s')."' reg_dt,
                                                        ifnull(b.unit_price, 0) * ifnull(c.unit_price_rate,0) + ifnull(c.unit_price_fixed,0) unit_price,
                                                        $factor_item_id related_factor_item_id
                                            FROM `factor_item` a
                                            join product_sva b on a.obj_item_id = b.product_id
                                            join product_additional c on c.obj_item_id = b.product_id
                                            WHERE factor_id = {$factor_id_decoded}
                                                and related_factor_item_id is null", false);
        // $product_additional_row = $db->query("Select    {$factor_id_decoded} factor_id, 
        //                                                 a.obj_item_add_id obj_item_id, 
        //                                                 a.amount*c.amount amount,
        //                                                 {$sess->get('auth')[0]['user_id']} register, 
        //                                                 '".date('Y-m-d H:i:s')."' reg_dt,
        //                                                 ifnull(b.unit_price, 0) * ifnull(a.unit_price_rate,0) + ifnull(a.unit_price_fixed,0) unit_price,
        //                                                 $factor_item_id related_factor_item_id
        //                                         from product_additional a
        //                                         join product_sva b on a.obj_item_add_id = b.product_id
        //                                         join factor_item c on a.obj_item_add_id = c.obj_item_id and c.factor_id = $factor_id_decoded
        //                                         Where a.obj_item_id = $product_id
        //                                         ", false);
        $factor_item_id = $db->insertArray('factor_item', $product_additional_row);

        // اعلام تخفیفات بر اساس جدول تخفیفات محصول
        $discount = $db->query("Select b.*
                                    from factor_item a                                
                                    join product_discount b 
                                        on a.obj_item_id = b.obj_item_id 
                                            and b.discount_type = 'BUY'
                                            and b.amount = (
                                                Select max(b.amount)
                                                from factor_item a                                
                                                    join product_discount b 
                                                        on a.obj_item_id = b.obj_item_id 
                                                            and b.discount_type = 'BUY'
                                                            and a.amount >= b.amount
                                                    Where a.factor_id = {$factor_id_decoded}                
                                            )
                                    Where a.factor_id = {$factor_id_decoded}
                                ");

        foreach($discount as $key => $value) {
            $discount_percent = $value['percent_rate'];
            $discount_price   = $value['fixed_rate'];
            $SQL =  "Update factor_item  set discount_percent = $discount_percent, discount_price = {$discount_price} Where factor_id = {$factor_id_decoded} and obj_item_id = {$value['obj_item_id']}";
            $db->exec($SQL);
        }

        // return '123';
        // بروزرسانی تخفیف ها

        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.product.add');

    // [X] حذف آیتم از فاکتور
    $app->post("/customer/factor/item/{factor_item_id}/delete", function($factor_item_id) use($app,$HASH_KEY){
        $hashid = new Hashids($HASH_KEY);
        $factor_item_id = $hashid->decode($factor_item_id)[0];

        $sess = new Session();
        $vendor_id = get_vendorcode();

        $_factor_call_type =  $sess->get('_factor_call_type');
        $_factor_call_type_is_customer = $_factor_call_type == 'customer' ? true : false;

        $db = DB::getConnection();

        // چک که قرارداد آیتم مربوطه به کاربری هست که وارد سیستم شده است
        $check_1  = $db->query("Select count(*) as cnt
                                from factor_item a 
                                join factor b on a.factor_id = b.factor_id
                                join contract c on b.contract_id = c.contract_id and c.vendor = {$vendor_id}
                                where a.factor_item_id = {$factor_item_id}
                                ")[0];
        
        // [ ] چک شود فاکتور تایید نشده باشد
        if($check_1['cnt'] <= 0 && $_factor_call_type_is_customer){
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }
        
        $db->delete('factor_item', array('factor_item_id'=>$factor_item_id));
        $db->delete('factor_item', array('related_factor_item_id'=>$factor_item_id));
        $db->delete('depo_send', array( 'source_id' => $factor_item_id, 'source_type' =>  'FACTOR'));
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.product.delete');

    // [X] حذف آیتم از پرداختی فاکتور
    $app->post("/customer/factor/payment/{factor_payment_id}/delete", function($factor_payment_id) use($app,$HASH_KEY){
        $hashid = new Hashids($HASH_KEY);
        $factor_payment_id = $hashid->decode($factor_payment_id)[0];

        // اگر فروشنده کد فروشندگی نداشت امکان حذف وجود نخواهد داشت
        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor_id) == 0){
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $db = DB::getConnection();
        // $check_1 = $db->query("Select Count(*) as cnt 
        //                         from factor_payway a
        //                         join factor b on a.factor_id = b.factor_id and b.register is null and b.confirm_dt is null
        //                         join contract c on b.contract_id = c.contract_id and c.vendor = {$vendor_id}
        //                         Where a.factor_payway_id = {$factor_payment_id}
        //                         ")[0];
        
        // if($check_1['cnt'] > 0){
            $db->delete('factor_payway', array('factor_payway_id' => $factor_payment_id));
        // }
        // $sess->getFlashBag()->add('error', "خطا در حذف پرداختی از فاکتور.");
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.payment.delete');

    // [X] حذف سند پرداخت
    $app->post("/customer/factor/document/{factor_document_id}/delete", function($factor_document_id) use($app,$HASH_KEY){
        $hashid = new Hashids($HASH_KEY);
        $factor_document_id = $hashid->decode($factor_document_id)[0];

        // اگر فروشنده کد فروشندگی نداشت امکان حذف وجود نخواهد داشت
        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor_id) == 0){
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $db = DB::getConnection();
        $check_1 = $db->query("Select Count(*) as cnt 
                                from factor_document a
                                join factor b on a.factor_id = b.factor_id and b.register is null and b.confirm_dt is null
                                join contract c on b.contract_id = c.contract_id and c.vendor = {$vendor_id}
                                Where a.factor_document_id = {$factor_document_id}
                                ")[0];
        
        if($check_1['cnt'] > 0){
            $db->delete('factor_document', array('factor_document_id' => $factor_document_id));
        }
        
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.document.delete');

    // MWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMWMW
    // [x]
    $app->post("/customer/{customer_id}/factor/{factor_id}/payment/add", function($customer_id, $factor_id) use($app,$HASH_KEY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id_encoded)[0];

        $factor_id_decoded = $hashids->decode($factor_id)[0];
        $sess = new Session();

        if(!isInteger($_POST['price'])){
            $sess->getFlashBag()->add('error', "مبلغ را صحیح وارد نمایید.");    
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }
        if($_POST['price']*1<=0){
            $sess->getFlashBag()->add('error', "مبلغ را صحیح وارد نمایید.");    
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }

        // اگر کاربر کد مشتری اختصاص داده نشده بود امکان مشاهده فرم فوق را نخواهند داشت
        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];

        // فاکتور باید ثبت نشده باشد
        // فاکتور باید تایید نشده باشد
        $db = DB::getConnection();
        // $product_list = $db->query("Select count(*) as cnt
        //                                 from factor a
        //                                 join contract b on a.contract_id = b.contract_id
        //                                 join contract_item c on b.contract_id = c.contract_id
        //                                 join product_sva d on c.obj_item_id = d.obj_item_id
        //                                 Where a.factor_id = {$factor_id_decoded} 
        //                                         and b.vendor = {$vendor_id}
        //                                         and a.buyer_id = {$customer_id}
        //                                         and a.register is null
        //                                         and a.confirmer is null
        //                             ")[0];
        // if($product_list['cnt']<=0){
        //     $sess->getFlashBag()->add('error', "خطای سیستم‌ای، مشخصات انتخاب شده با کاربری شما مطابقت ندارد");
        //     return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        // }

        $_POST['factor_id'] = $factor_id_decoded;

        if ($_POST['pay_type'] == 'CASH') {
            unset($_POST['bank_id']);
            unset($_POST['no']);
        }else
        if ($_POST['pay_type'] == 'CART') {
            // unset($_POST['bank_id']);
        }
        
        $_POST['register'] = get_userid();
        $db->insert('factor_payway', $_POST);
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.payment.add');

    // [x]
    $app->post("/customer/{customer_id}/factor/{factor_id}/document/add", function($customer_id, $factor_id) use($app,$HASH_KEY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id_encoded)[0];
        
        $hashid = new Hashids($HASH_KEY);
        $factor_id_decoded = $hashid->decode($factor_id)[0];

        // اگر فروشنده کد فروشندگی نداشت امکان حذف وجود نخواهد داشت
        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];
        if(strlen($vendor_id) == 0){
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }

        // چک شماره قرارداد متعلق به فروشنده ای که وارد سیستم شده است باشد
        // و فاکتور مورد نظر ثبت و تایید نشده باشد
        $db = DB::getConnection();
        $check_1 = $db->query("Select Count(*) as cnt 
                                from factor b
                                join contract c on b.contract_id = c.contract_id and c.vendor = {$vendor_id}
                                Where b.factor_id = {$factor_id_decoded}
                                        and b.register is null 
                                        and b.confirm_dt is null
                                ")[0];
        
        if($check_1['cnt'] < 0){
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }

        // چک کردن پسوند و محتوای فایل آپلود شده

        $_POST['factor_id'] = $factor_id_decoded;
        $_POST['register']  = get_userid();
        $document_id = $db->insert('factor_document', $_POST);
        $document_id_encoded = $hashid->encode($document_id);

        $_ext  = pathinfo($_FILES['uri']['name'])['extension'];
        $_src  = $_FILES['uri']['tmp_name'];
        $_dest = "./uploads/sales/pay_{$factor_id_decoded}_{$document_id}.{$_ext}";
        $_dest_enc = "pay_{$factor_id}_{$document_id_encoded}.{$_ext}";

        if(!@copy($_src, $_dest)){
            // $errors= error_get_last();
            // print_r($errors);
            // return '---';
        }
        $hash = md5( file_get_contents($_dest) );

        $db->update('factor_document', 
                            array(
                                    'uri' => $_dest_enc,
                                    'hash' => $hash
                            ), 
                            array('factor_document_id' => $document_id));

        return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
    })->bind('customer.factor.document.add');

    // [x]
    $app->get("/upload/{file_name}", function($file_name) use($app, $HASH_KEY){
        $explode = explode('_', $file_name);

        if($explode[0] == 'payment'){
            $hashid = new Hashids($HASH_KEY);
            $id_1 = $hashid->decode($explode[1])[0];
            $ext  = strtolower($explode[2]);
            $file = "./uploads/sales/obj_document_{$id_1}.{$ext}";
        }else{
            $hashid = new Hashids($HASH_KEY);
            $id_1 = $hashid->decode($explode[1])[0];
            $id_2 = $hashid->decode($explode[2])[0];
            $ext  = strtolower($explode[3]);
            $file = "./uploads/sales/{$explode[0]}_{$id_1}_{$id_2}.{$ext}";
        }

        if($explode[3] == 'pdf'){
            header('Content-type: application/pdf');
        }else if($explode[3] == 'jpg'){
            header('Content-type: image/jpeg');
        }else if($explode[3] == 'gif'){
            header('Content-type: image/gif');
        }else if($explode[3] == 'png'){
            header('Content-type: image/png');
        }
        header('Content-disposition: inline; filename=file.pdf');
        $data = readfile($file);

        return '';
    })->bind('customer.factor.document.show')->assert('file_name', '.*');

    // [ ] ثبت نهایی فاکتور توسط فروشنده
    $app->post("/customer/{customer_id}/factor/{factor_id}/save", function($factor_id, $customer_id) use($app, $HASH_KEY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id_encoded)[0];

        $hashid = new Hashids($HASH_KEY);
        $factor_id_decoded = $hashid->decode($factor_id)[0]*1;
        
        // [ ] اگر شهر انتخاب شود باید آدرس و تلفن و تحویل گیرنده نیز به صورت صحیح وارد شود
        // اگر فروشنده کد فروشندگی نداشت امکان حذف وجود نخواهد داشت
        $sess = new Session();
        $vendor_id = get_vendorcode();
        if(strlen($vendor_id) == 0){
            return $app->redirect("/customer");
        }

        $db = DB::getConnection();

        $factor_price = $db->query("Select sum(price) as price from factor_item where factor_id = {$factor_id_decoded}")[0]['price'] * 1;
        $factor_pay   = $db->query("Select sum(price) as price from factor_payway where factor_id = {$factor_id_decoded}")[0]['price'] * 1;

        $customer_reminded_account = $db->query("Select Sum(Credit)-Sum(Debit) reminded From customer_payment Where obj_item_id = {$customer_id}")[0]['reminded'];
        $factor_pay = $factor_pay+$customer_reminded_account;

        if($factor_price > $factor_pay){
            $sess->getFlashBag()->add('error', "پرداختی فاکتور به صورت صحیح ثبت نشده است");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        // اگر مشتری وارد سیستم شده قرارداد فعال نداشته باشد به صفحه اصلی هدایت خواهد شد
        // تصویب شده باشد و متوقف نشده باشد
        // تاریخ قرارداد فعلا چک نمی‌شود
        $contract = $db->query("Select * from contract where type = 'SELL' and vendor = {$vendor_id} and sign_dt is not null and stop_dt is null")[0];
        if(count($contract) == 0){
            $sess->getFlashBag()->add('error', "قرارداد فروش فعال ندارید");
            return $app->redirect('/customer');
        }

        // اگر خریدار ثبت فاکتور شده متعلق به کاربر فوق نمی باشد
        // برای مشتری که غیر فعال شده است نمی توان فاکتور صادر نمود        
        $customer  = $db->query("Select * from customer_sva where obj_item_id = {$customer_id} and status = 1 and reagent = {$vendor_id}")[0];
        if(count($customer) == 0){
            $sess->getFlashBag()->add('error', "دسترسی به فاکتور فروش درخواست شده را ندارید");
            return $app->redirect('/customer');
        }

        // اگر فاکتور ثبت شده است امکان ویرایش وجود نداشته باشد
        // به صفحه لیست فاکتورهای پیش نویس منتقل شود
        $factor = $db->query("Select a.*, b.*, c.title city_name
                                from factor a
                                join customer_sva b on a.buyer_id = b.obj_item_id
                                left join obj_item c on b.city_id = c.obj_item_id
                                where a.factor_id = {$factor_id_decoded} and a.register is null and a.confirmer is null")[0];
        if(count($factor) == 0){
            // Hack
            $sess->getFlashBag()->add('error', "فاکتور قبلا ثبت شده است و امکان ایجاد تغییرات در آن را ندارید");
            return $app->redirect('/customer');
        }

        // اگر آیتم دارای اجزا فروش نیست امکان ثبت نداشته باشد
        $check_1 = $db->query("Select count(*) as cnt from factor_item where factor_id = {$factor_id_decoded}")[0];
        if($check_1['cnt'] == 0){
            $sess->getFlashBag()->add('error', "فاکتور فروش خالی می‌باشد");
            return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        }

        // اگر دارای روش پراخت نیست فاکتور ثبت نشود
        // $check_1 = $db->query("Select count(*) as cnt from factor_payway where factor_id = {$factor_id_decoded}")[0];
        // if($check_1['cnt'] == 0){
        //     $sess->getFlashBag()->add('error', "پرداختی برای فاکتور فوق ثبت نشده است");
        //     return $app->redirect("/customer/{$customer_id_encoded}/factor/{$factor_id}");
        // }

        // [X] چک شود فاکتور فروش با پرداختی ها بالانس باشد
        // [ ] اگر دارای روش پرداخت چک و کارت به کارت و یا کارت خوان است بدون آپلود مستندات ثبت نشود

        $seller_factor_id = $db->query("Select getNextCustomSeq('seller_factor_id', '{$vendor_id}') seller_factor_id")[0];
        $seller_factor_id = $seller_factor_id['seller_factor_id'];
        $_POST['seller_factor_id']  = $seller_factor_id;
        $_POST['register']          = get_userid();
        $_POST['reg_dt']            = curdate();
        $_POST['reg_status']        = 'CONFIRM';

        $db->update('factor', $_POST, array('factor_id' => $factor_id_decoded));
                                    
        $db->update('pre_factor', array('status' => 1), array("buyer_id" => $customer_id));

        $seller_factor_id = formatfactor($seller_factor_id);
        $sess->getFlashBag()->add('info', "فاکتور به شماره {$seller_factor_id} با موفقیت ثبت گردید");

        $sms_reciever = $db->query("Select *
                                    From user_chart uc
                                    join user u on uc.user_id = u.user_id
                                    where uc.chart_id = 32
                                    ");
        foreach ($sms_reciever as $key => $value) {
            $message = sprintf("همکار محترم، %s\n شناسه درخواست %s منتظر تایید مالی می‌باشد", $value['name'], $factor_id_decoded);
            send_sms($value['mobile'], $message, true);
        }
        return $app->redirect("/customer");
    })->bind('customer.factor.save');

    $app->post("/customer/factor/address/{customer_id}/{factor_id}/save", function($customer_id, $factor_id) use($app, $HASH_KEY){
        $hashids     = new Hashids($HASH_KEY);
        $customer_id_dec = $hashids->decode($customer_id)[0];
        $factor_id_dec   = $hashids->decode($factor_id)[0];
        $_POST['factor_id'] = $factor_id_dec;

        $db = DB::getConnection();
        $db->insert('factor_address', $_POST);

        $sess = new Session();
        $sess->getFlashBag()->add('success', "آدرس جدید اضافه شد");
        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.address.save');

    // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    // [ ] ثبت فاکتور فروش
    $app->get("/customer/factor/confirm/sale", function() use($app){
        $user_cart_city = get_user_chart_city();        
        $v_city_id = 1;
        if(count($user_cart_city)){
            $v_city_id = implode(",", get_user_chart_city());
        }
        if($v_city_id == ''){
            $v_city_id = 1;
        }
        
        $db = DB::getConnection();
        $row = $db->query("Select a.factor_id, a.seller_factor_id, a.buyer_id, a.seller_buyer_id, a.customer_name, a.codemeli, a.phone, a.mobile, sum(a.amount) amount, sum(a.sended) sended, sum(a.amount)-sum(a.sended) reminded
                                    , b.city_id, c.name city_name
                                    , f.acc_confirm_dt
                                From factor_item_balance_sva a
                                left join customer_sva b on a.buyer_id = b.obj_item_id
                                left join obj_item c on b.city_id = c.obj_item_id
                                left join factor f on f.factor_id = a.factor_id
                            Group by a.factor_id, a.seller_factor_id, a.buyer_id, a.seller_buyer_id, a.customer_name, a.codemeli, a.phone, a.mobile, b.city_id, f.acc_confirm_dt
                            Having sum(a.amount)-sum(a.sended) > 0");

        return $app['twig']->render('admin/customer/customer.confirm.sale.list.twig', array(
                            'row' => $row,
                        ));
    })->bind('customer.factor.confirm.sale.index');

    $app->post("/customer/{customer_id}/factor/{factor_id}/confirm/sale", function($customer_id, $factor_id) use($app){
        return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/sale");
    })->bind('customer.factor.confirm.sale.show');

    $app->post("/customer/{customer_id}/factor/{factor_id}/confirm/sale/process", function($customer_id, $factor_id) use($app,$HASH_KEY,$COMPANY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id_encoded)[0];        

        $factor_id_encoded = $factor_id;
        $factor_id = $hashids->decode($factor_id_encoded)[0];

        $sess = new Session();
        $vendor_id = $sess->get('auth')[0]['vendor_code'];

        // [ ] چک شود اگر فاکتور دارای محموله اختصاص داده نشده است تایید خورده نشود
        $db = DB::getConnection();
        $db->update('factor', array(
            'sale_confirmer'   => get_userid(),
            'sale_confirm_dt'  => curdate(),
        ), array('factor_id' => $factor_id));


        // xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        $check_1 = $db->query("Select a.*
                                From customer_sva a
                                join factor b on a.obj_item_id = b.buyer_id and factor_id = {$factor_id}
                                ")[0];
        $mobile_number = $check_1['mobile'];
        $name = $check_1['title'];

        $mobile_number = $check_1['mobile'];
        $name          = $check_1['title'];
        $reagent_title = $check_1['reagent_title'];
        $sex_type      = $check_1['sex_title'];
        $brand_name    = $check_1['brand_name'];
        $brand_slung   = $check_1['brand_slung'];
        
        if(check_mobile($mobile_number)){
            $message = sprintf("مشتری گرامی %s %s\nفاکتور خرید شما به شماره %s در سامانه مالی %s ثبت گردید، منتظر تماس همکاران ما جهت ارسال محصول خریداری شده بمانید. از حسن اعتماد شما سپاسگذاریم.\n%s", $sex_type, $name, '12'.$factor_id, $brand_name, $brand_slung);
            send_sms($mobile_number, $message);
        }

        $sess->getFlashBag()->add('success', sprintf("فاکتور %s به شماره %s با موفیت ثبت گردید",$name,$factor_id));

        return $app->redirect("/customer/factor/confirm/sale");
    })->bind('customer.factor.confirm.sale.confirm');

    // [x]
    $app->post("/customer/factor/confirm/sale/assign/depo", function() use($app){
        $sess = new Session();
        $db = DB::getConnection();

        // ..............................
        // [ ] چک موجودی انبار
        // $factor_item_id = $_POST['factor_item_id'] * 1;
        // $check = $db->query("Select count(*) as cnt from factor_depo_balance where balance > 0 and amount <= balance and factor_item_id = {$factor_item_id}")[0];
        // if($check['cnt'] <= 0){
        //     $sess->getFlashBag()->add('error', "کسری موجودی انبار");
        //     return $app->redirect($_SERVER['HTTP_REFERER']);
        // }

        if($_POST['depo'] == ''){
            $sess->getFlashBag()->add('error', "انبار انتخاب نشده است و یا موجودی انبار برای کالای فوق وجود ندارد");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $db = DB::getConnection();
        $city_id = $_POST['city_id'];
        $factor_item_id = $_POST['factor_item_id'];
        $depo_id = $_POST['depo'];

        $row  = $db->query("Select a.factor_item_id, a.factor_id, a.obj_item_id, a.amount, b.*, c.title depo_name
                            from factor_item a
                            join depo_balance_city_sva b on a.obj_item_id = b.obj_item_id and b.city_id = {$city_id} and b.depo_id = {$depo_id}
                            left join obj_item c on c.obj_item_id = b.depo_id
                            Where a.factor_item_id = {$factor_item_id}
                            ")[0];

        // چک شود مقدار وارد شده واقعی باشد و توسط کاربر تغییر داده نشده باشد
        if($_POST['amount'] > $row['balance']){
            $sess->getFlashBag()->add('error', "انبار موجودی ندارد");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        if($_POST['amount'] * 1 <= 0){
            $sess->getFlashBag()->add('error', "میزان سفارش انتخاب نشده است");
            return $app->redirect($_SERVER['HTTP_REFERER']);
        }

        $_POST['goods']       = $db->query("Select obj_item_id from factor_item where factor_item_id = {$_POST['factor_item_id']}")[0]['obj_item_id'];
        $_POST['source_type'] = 'FACTOR';
        $_POST['source_id']   = $_POST['factor_item_id'];
        $_POST['depo_id']     = $_POST['depo'];
        $_POST['register']    = get_userid();
        $_POST['reg_dt']      = get_curdate();
        unset($_POST['factor_item_id']);
        unset($_POST['depo']);
        
        // $db->update('factor_item', array('depo_id'=> $_POST['depo']*1,), array('factor_item_id' => $factor_item_id));
        $db->insert('depo_send', $_POST);

        return $app->redirect($_SERVER['HTTP_REFERER']);
    })->bind('customer.factor.confirm.sale.assign.depo');

    // [x] لیست منتظر تایید فاکتور توسط مالی
    $app->get("/customer/factor/confirm/account", function() use($app){
        $db = DB::getConnection();
        //[x]todo: فقط فاکتورهایی که چک دارند و استعلام + دارند نمایش داده شوند و یا نقد خریداری شده اند
        // [ ] چک شود اگر فروشنده اعتبار ندارد فاکتور تاییدش مشاهده نشود

        $row = $db->query("Select    a.factor_id
                                    , a.seller_factor_id
                                    , a.buyer_id
                                    , b.seller_buyer_id
                                    , b.codemeli, b.phone, b.mobile
                                    , b.title as customer_name
                                    , d.title as seller_name
                                    , e.title as city_name
                                    , csva.credit_status
                                    , csva.reminded
                            from factor a
                            join customer_sva b on a.buyer_id = b.obj_item_id
                            join contract c on a.contract_id = c.contract_id
                            join obj_item d on c.vendor = d.obj_item_id and d.status = 1
                            left join obj_item e on b.city_id = e.obj_item_id
                            left join credit_sum_sva csva on csva.vendor_buyer_id = c.vendor
                            Where a.register is not null
                                and a.reg_status = 'CONFIRM'
                                and a.acc_confirmer is null
                                -- and a.factor_id in (SELECT factor_id
                                --                    FROM factor_inquiry_sva a
                                --                  Where inquiry_status_sign = 1
                                --                  )
                            Group by a.factor_id, a.seller_factor_id, a.buyer_id, b.seller_buyer_id, b.codemeli, b.phone, b.mobile, b.title, d.title, e.title
                                     , csva.credit_status, csva.reminded
                            ");
        return $app['twig']->render('admin/customer/customer.confirm.account.list.twig', array('row' => $row,));
    })->bind('customer.factor.confirm.account.index');

    $app->post("/customer/{customer_id}/factor/{factor_id}/confirm/account", function($customer_id, $factor_id) use($app){
        return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/account");
    })->bind('customer.factor.confirm.account.show');

    $app->post("/customer/{customer_id}/factor/{factor_id}/confirm/account/process", function($customer_id, $factor_id) use($app,$HASH_KEY,$COMPANY){
        $hashids = new Hashids($HASH_KEY);
        $customer_id_encoded = $customer_id;
        $customer_id = $hashids->decode($customer_id_encoded)[0];        

        $factor_id_encoded = $factor_id;
        $factor_id = $hashids->decode($factor_id_encoded)[0];
        
        $db = DB::getConnection();

        // ثبت درصورتی انجام شود که فاکتور فوق استعلام تایید شده داشته باشد
        // درصورتی که فاکتور حاوی چک باشد استعلام چک میشود

        $row_check_1 = $db->query("SELECT Count(*) as cnt
                                    FROM factor_inquiry_sva a
                                    Where a.factor_id = {$factor_id}
                                    group by factor_id
                                    having count(*) = sum(a.inquiry_status_sign)")[0];
        if($row_check_1['cnt'] == 0){
            return $app->redirect('/customer/factor/confirm/account');
        }

        $sess = new Session();

        if($_POST['acc_status'] == 'CONFIRM'){
            $_POST['acc_status'] = 1;
        }else{
            $_POST['acc_status'] = 0;
        }
        $_POST['acc_confirm_dt'] = curdate();
        $_POST['acc_confirmer'] = get_userid();

        $db->update('factor', $_POST, array('factor_id' => $factor_id));

        // Send SMS
        $check_1 = $db->query("Select a.*, b.seller_factor_id
                                From customer_sva a
                                join factor b on a.obj_item_id = b.buyer_id and factor_id = {$factor_id}
                                ")[0];

        $COMPANY        = $GLOBALS['COMPANY'];
        $COMPANY_SITE   = $GLOBALS['COMPANY_SITE'];
        $mobile_number  = $check_1['mobile'];
        $name           = $check_1['title'];
        $sex_type       = $check_1['sex_title'];
        $sell_factor_id = formatfactor($check_1['seller_factor_id']);
        $shobe          = $check_1['reagent_title'];;

        if($_POST['acc_status'] == 1){
            $sms_reciever = $db->query("Select *
                    From user_chart uc
                    join user u on uc.user_id = u.user_id
                    where uc.chart_id = 4
            ");
            foreach ($sms_reciever as $key => $value) {
                $message = sprintf("همکار گرامی، %s \n درخواست %s %s به شناسه %s منتظر اختصاص انبار می‌باشد", $value['name'], $sex_type, $name, $factor_id);
                send_sms($value['mobile'], $message, true);
            }
        }

        if(check_mobile($mobile_number)){
            if($_POST['acc_status'] == 'CONFIRM'){
                $message = sprintf("مشتری گرامی %s %s \n فاکتور شما به شماره %s صادر و به فروشگاه %s %s ارسال گردید. منتظر تماس همکاران ما جهت ارسال کالا باشید. \n با تشکر از انتخاب شما", $sex_type, $name, $sell_factor_id, $COMPANY_SITE, $COMPANY);
                send_sms($mobile_number, $message);
            }
        }

        if($_POST['acc_status'] == 'CONFIRM'){
            $sms_reciever = $db->query("Select *
                    From user_chart uc
                    join user u on uc.user_id = u.user_id
                    where uc.chart_id = 4
            ");
            foreach ($sms_reciever as $key => $value) {
                $message = sprintf("همکار محترم، %s\n درخواست %s %s به شناسه %s منتظر اختصاص انبار می‌باشد.", $value['name'], $sex_type, $name);

                send_sms($value['mobile'], $message, true);
            }
        }

        return $app->redirect("/customer/factor/confirm/account");
    })->bind('customer.factor.confirm.account.confirm');

    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // Document Control
    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // [x] فرم دریافت مدارک از فروشندگان
    $app->get("/seller/receipt", function() use($app){
        $db        = DB::getConnection();
        $sess      = new Session();
        $user_city = $sess->get('user_city');

        // [ ] اگر شهری پیگیری کننده ندارد برای همه افراد مشاهده شود
        $row = $db->query("Select fd.*
                            From factor_document_waited_sva fd
                            join vendor_buyer_sva vb on vb.obj_item_id = fd.vendor and vb.city_id in ({$user_city})
                            ");
        return $app['twig']->render('admin/customer/receipt.index.twig', array(
            'row'=>$row,
        ));
    })->bind('customer.factor.doc.receipt.index');

    // چاپ مدارکی که هنوز از فروشنده تحویل نشده اند
    $app->get("/seller/{seller_id}/receipt/print", function($seller_id) use($app){
        $db = DB::getConnection();

        $vendor    = get_vendorcode();
        $dt        = curdate();

        $db->exec("Update factor 
                    set receipt_doc_printer_id = {$vendor}, receipt_doc_print_dt = '{$dt}' 
                    Where factor_id in (Select factor_id from factor_document_waited_sva where vendor = {$seller_id})");

        $row_parent = $db->query("Select fd.*
                            From factor_document_waited_sva fd
                            join vendor_buyer_sva vb on vb.obj_item_id = fd.vendor 
                            Where fd.vendor = {$seller_id}
                    ")[0];

        $row = $db->query("Select *
                            from factor_payway_sva
                            Where   vendor = {$seller_id}
                                    and pay_type in ('CART', 'CHEQUE','CASH') 
                                    and pay_level = 'FACTOR'
                            Order by factor_id, buyer_id
                        ");

        $row_doc = $db->query("Select *
                                from factor_document
                                where factor_id in (Select factor_id from factor_payway_sva Where vendor = {$seller_id} and pay_type in ('CART', 'CHEQUE'))
                                order by factor_id");

        return $app['twig']->render('admin/customer/receipt.print.twig', array(
            'row'=>$row,
            'row_doc'=>$row_doc,
            'row_parent'=>$row_parent,
        ));

    })->bind('customer.factor.doc.receipt.print');


    // فرم دریافت مدارک از فروشندگان
    // [ ]todo: برگشت اعتبار مشتری
    $app->get("/seller/receipt/confirm", function() use($app){

        $sess = new Session();
        $user_city = $sess->get('user_city');
        $db = DB::getConnection();
        $row = $db->query("Select e.factor_payway_id, a.vendor, b.title vendor_name, b.province_id province_id, b.city_id, c.title city_name, b.address
                                , (substr(d.seller_factor_id, 11, 5)*1) seller_factor_id
                                , (d.factor_id) factor_id
                                , TIMESTAMPDIFF(HOUR, (d.reg_dt), Now()) date_dif
                                , (if(e.pay_type = 'CHEQUE', e.price, 0)) price_cheque
                                , (if(e.pay_type = 'CART', e.price, 0)) price_cart
                                , vb.city_id
                                , vb.name customer_name
                            from contract a
                            join vendor_buyer_sva b on a.vendor = b.obj_item_id and b.city_id in ({$user_city})
                            join obj_item c on b.city_id = c.obj_item_id
                            join factor d on d.contract_id = a.contract_id and d.acc_status > 0 and d.acc_confirmer is not null -- and d.sale_confirmer is not null
                            join factor_payway e on d.factor_id = e.factor_id and e.receipe_id is null and e.pay_type in ('CHEQUE','CART') and e.pay_level = 'FACTOR'
                            join vendor_buyer_sva vb on vb.obj_item_id = d.buyer_id
                        ");

        return $app['twig']->render('admin/customer/receipt.confirm.twig', array(
            'row'=>$row,
        ));
    })->bind('customer.factor.doc.receipt.confirm');

    $app->post("/seller/receipt/confirm", function() use($app){
        $where    = "";
        $seprator = "";
        foreach ($_POST['item'] as $key => $value) {
            $where   .= $value . ",";
        }
        $where .= "-1";


        $sess    = new Session();
        $user_id = get_userid();
        $dt      = curdate();

        $db = DB::getConnection();
        $db->exec("Update factor_payway 
                    set receipe_id = {$user_id}, receip_dt = '{$dt}'
                    Where factor_payway_id in ($where)
                        and receipe_id is null
                        and receip_dt is null");
        return redirect($app, '/seller/receipt');
    })->bind('customer.factor.doc.receipt.confirm.post');

    // ارسال مدارک
    $app->get("/seller/receipt/send", function() use($app){
        $db = DB::getConnection();
        $sess = new Session();
        $user_city = $sess->get('user_city');
        $row = $db->query("Select e.factor_payway_id, a.vendor, b.title vendor_name, b.province_id province_id, b.city_id, c.title city_name, b.address
                                , (substr(d.seller_factor_id, 11, 5)*1) seller_factor_id
                                , (d.factor_id) factor_id
                                , e.pay_type
                                , TIMESTAMPDIFF(HOUR, (d.reg_dt), Now()) date_dif
                                , e.price price
                                , (if(e.pay_type = 'CHEQUE', e.price, 0)) price_cheque
                                , (if(e.pay_type = 'CART', e.price, 0)) price_cart
                                , (if(e.pay_type = 'CASH', e.price, 0)) price_cash
                                , vb.name customer_name
                            from contract a
                            join vendor_buyer_sva b on a.vendor = b.obj_item_id and b.city_id in ({$user_city})
                            join obj_item c on b.city_id = c.obj_item_id
                            join factor d on d.contract_id = a.contract_id and d.acc_status > 0 and d.acc_confirmer is not null -- and d.sale_confirmer is not null
                            join factor_payway e on d.factor_id = e.factor_id and e.receipe_id is not null and e.pay_type in ('CHEQUE','CART') and e.receipe_id is not null and e.receive_doc_id is null
                            join vendor_buyer_sva vb on vb.obj_item_id = d.buyer_id
                            ");

        return $app['twig']->render('admin/customer/receipt.send.twig', array(
            'row'=>$row,
        ));
    })->bind('customer.factor.doc.receipt.send');

    $app->post("/seller/receipt/send", function() use($app){
        // return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/sale");
        $sess = new Session();
        $user_id          = get_userid();
        $factor_payway_id = $_POST['factor_payway_id']*1;
        $desc = $_POST['desc'];

        $where = '';
        foreach ($_POST['item'] as $key => $value) {
            $where .= $value.',';
        }
        $where .= '-1';

        $dt = curdate();

        $db = DB::getConnection();
        $db->exec("Update factor_payway 
                    set receive_doc_id = {$user_id}, receieve_doc_dt = '{$dt}', receieve_doc_description = '$desc'
                    Where factor_payway_id in ({$where})
                        and receipe_id is not  null
                        and receip_dt is not null
                        and receive_doc_id is null
                        ");
        return $app->redirect("/seller/receipt/send");
    })->bind('customer.factor.doc.receipt.send.post');
    // دریافت مدارک مالی
    $app->get("/seller/receipt/receive", function() use($app){
        $db = DB::getConnection();
        $row = $db->query("Select e.factor_payway_id, a.vendor, b.title vendor_name, b.province_id province_id, b.city_id, c.title city_name, b.address
                                , (substr(d.seller_factor_id, 11, 5)*1) seller_factor_id
                                , (d.factor_id) factor_id
                                , TIMESTAMPDIFF(HOUR, (d.reg_dt), Now()) date_dif
                                , e.pay_type
                                , e.price
                                , (if(e.pay_type = 'CHEQUE', e.price, 0)) price_cheque
                                , (if(e.pay_type = 'CART', e.price, 0)) price_cart
                                , vb.name customer_name
                            from contract a
                            join vendor_buyer_sva b on a.vendor = b.obj_item_id
                            join obj_item c on b.city_id = c.obj_item_id
                            join factor d on d.contract_id = a.contract_id and d.acc_status > 0 and d.acc_confirmer is not null -- and d.sale_confirmer is not null
                            join vendor_buyer_sva vb on vb.obj_item_id = d.buyer_id
                            join factor_payway e on d.factor_id = e.factor_id 
                                                    and e.receipe_id is not null 
                                                    and e.pay_type in ('CHEQUE','CART') 
                                                    and e.receive_doc_id is not null
                                                    and e.receive_acc_dt is null
                                                    and e.receive_acc_id is null
                            ");
        return $app['twig']->render('admin/customer/receipt.receive.twig', array(
            'row'=>$row,
        ));
    })->bind('customer.factor.doc.receipt.receive');
    $app->post("/seller/receipt/receive", function() use($app){
        $sess = new Session();
        $user_id          = get_userid();
        $factor_payway_id = $_POST['factor_payway_id']*1;
        $desc = $_POST['desc'];

        $dt = curdate();

        $where = '';
        foreach ($_POST['item'] as $key => $value) {
            $where .= $value.',';
        }
        $where .= '-1';

        $db = DB::getConnection();
        $db->exec("Update factor_payway 
                    set receive_acc_id = {$user_id}, receive_acc_dt = '{$dt}', receive_acc_description = '$desc'
                    Where factor_payway_id in ($where)
                        and receipe_id is not  null
                        and receip_dt is not null
                        and receive_doc_id is not null
                        and receive_acc_id is null
                        ");
        return $app->redirect("/seller/receipt/receive");
    })->bind('customer.factor.doc.receipt.receive.post');
    // وضعیت مدارک
    $app->get("/seller/receipt/list", function() use($app){
        $db = DB::getConnection();
        $row = $db->query("Select e.factor_payway_id, a.vendor, b.title vendor_name, b.province_id province_id, b.city_id, c.title city_name, b.address
                                , (substr(d.seller_factor_id, 11, 5)*1) seller_factor_id
                                , (d.factor_id) factor_id
                                , TIMESTAMPDIFF(HOUR, (d.reg_dt), Now()) date_dif
                                , (if(e.pay_type = 'CHEQUE', e.price, 0)) price_cheque
                                , (if(e.pay_type = 'CART', e.price, 0)) price_cart
                                , Case
                                    When e.receipe_id is     null and e.receive_doc_id is     null Then 'تحویل فروشنده'
                                    When e.receipe_id is not null and e.receive_doc_id is     null Then 'آماده ارسال'
                                    When e.receipe_id is     null and e.receive_doc_id is not null Then 'خطا'
                                    When e.receipe_id is not null and e.receive_doc_id is not null Then 'آماده دریافت مالی'
                                End status
                            from contract a
                            join vendor_buyer_sva b on a.vendor = b.obj_item_id
                            join obj_item c on b.city_id = c.obj_item_id
                            join factor d on d.contract_id = a.contract_id and d.acc_status > 0 and d.acc_confirmer is not null -- and d.sale_confirmer is not null
                            join factor_payway e on d.factor_id = e.factor_id 
                                                    -- and e.receipe_id is not null 
                                                    -- and e.receive_doc_id is not null
                                                    and e.pay_type in ('CHEQUE','CART') 
                                                    and e.receive_acc_dt is null
                                                    and e.receive_acc_id is null
                            ");
        return $app['twig']->render('admin/customer/receipt.list.twig', array(
            'row'=>$row,
        ));
    })->bind('customer.factor.doc.receipt.list');
    

    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // DEPO Control
    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    $app->get("/customer/factor/depo/ready", function($customer_id, $factor_id) use($app){
        // return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/sale");
        return '-';
    })->bind('customer.factor.depo.ready');
    $app->get("/customer/factor/depo/exit", function($customer_id, $factor_id) use($app){
        
        return '-';
        // return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/sale");
    })->bind('customer.factor.depo.exit');
    $app->get("/customer/factor/depo/exit", function($customer_id, $factor_id) use($app){
        
        return '-';
        // return $app->redirect("/customer/{$customer_id}/factor/{$factor_id}/sale");
    })->bind('customer.factor.depo.recieve');

    $app->get("/customer/factor/depo/balance/{city_id}/{factor_item_id}", function($city_id, $factor_item_id) use($app){
        // [ ] جک شود کد شهر وارد شده برای فاکتور فوق باشد
        // [ ] چک شود شماره فاکتور قبلا تعیین تکلیف نشده باشد
        // [ ] مانده فاکتور چک شود
        $db = DB::getConnection();
        $row  = $db->query("Select a.factor_item_id, a.factor_id, a.obj_item_id, a.amount, b.*, c.title depo_name
                            from factor_item a
                            join depo_balance_city_sva b on a.obj_item_id = b.obj_item_id and b.city_id = {$city_id}
                            left join obj_item c on c.obj_item_id = b.depo_id
                            Where a.factor_item_id = {$factor_item_id}
                            ");
        return json_encode($row);
    })->bind('customer.factor.depo.balance')->value('factor_item_id','')->value('city_id','');
    
    
    $app->post("/customer/pre-factor", function() use($app,$HASH_KEY){
        $vendor = get_vendorcode();

        $hashids = new Hashids($HASH_KEY);
        $_POST['customer_id'] = $hashids->decode($_POST['customer_id'])[0];

        $db = DB::getConnection();

        $index = 0;
        foreach ($_POST['product_id'] as $key => $value) {

            $contract_items = $db->query("Select max(p.unit_price) unit_price
                                            from contract c
                                            join contract_item ci on c.contract_id = ci.contract_id
                                            join product_sva p on ci.obj_item_id = p.obj_item_id
                                            Where c.vendor = {$vendor}
                                                and c.stop_dt is null
                                                and c.sign_dt is not null
                                                and c.type = 'SELL'
                                                and ci.obj_item_id = {$_POST['product_id'][$index]}
                                            ")[0];
            $insert = array(
                'buyer_id'    => $_POST['customer_id'],
                'obj_item_id' => $_POST['product_id'][$index],
                'unit_price'  => $contract_items['unit_price'],
                'amount'      => $_POST['amount'][$index],
                'register'    => get_userid()
            );
            $index++;
            $db->insert('pre_factor', $insert);
        }

        return redirect($app);
    })->bind('customer.pre.factor');
