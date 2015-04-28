//
//  AppDelegate.swift
//  __DEV__daeious-event-app
//
//  Created by Alexander Warren Chick on 4/23/15.
//  Copyright (c) 2015 The Intro Game LLC. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?


    func application(                    application: UIApplication,
         didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?)
        -> Bool {
        // Override point for customization after application launch.
        
            
            
            
            
//        var rootURL = "https://burning-fire-8681.firebaseio.com/see-again-choices-R1"
//        // remove any currently existing child data nodes
//        var root_ref = Firebase(url: rootURL)
//        root_ref.removeValue()
//            
//        for user_num in 1...100 {
//            
//            var event_user_num_str = ""
//            
//            if user_num < 10 {
//                event_user_num_str = "00" + String(user_num)
//            } else if user_num < 100 {
//                event_user_num_str = "0" + String(user_num)
//            } else {
//                event_user_num_str = String(user_num)
//            }
//            
//            var URL_no = rootURL + "/users/user" + event_user_num_str + "/no"
//            var URL_mn = rootURL + "/users/user" + event_user_num_str + "/mn"
//            var URL_my = rootURL + "/users/user" + event_user_num_str + "/my"
//            var URL_yes = rootURL + "/users/user" + event_user_num_str + "/yes"
//            
//            var ref_no = Firebase(url:URL_no)
//            var ref_mn = Firebase(url:URL_mn)
//            var ref_my = Firebase(url:URL_my)
//            var ref_yes = Firebase(url:URL_yes)
//            
//            for (key, value) in [ref_no:13, ref_mn:11, ref_my:8, ref_yes:14] {
//                key.setValue(value)
//            }
//            
//            println("usernum: \(event_user_num_str)")
//            
//            for ref in [ref_no, ref_mn, ref_my, ref_yes] {
//                ref.observeEventType(.Value, withBlock: {
//                    snapshot in
//                    println("\(snapshot.key) -> \(snapshot.value)")
//                })
//            }
//            
//        }
//
//        var URL_no = rootURL + "/users/user1/no"
//        var URL_mn = rootURL + "/users/user1/mn"
//        var URL_my = rootURL + "/users/user1/my"
//        var URL_yes = rootURL + "/users/user1/yes"


            
//        for (key, value) in [ref_no:12, ref_mn:1, ref_my:10, ref_yes:4] {
//            key.setValue(value) }
//        //user1.setValue(["no": 12, "maybe-no": 1, "maybe-yes": 10, "yes": 4])
//            
//        // Read data and react to changes
//        ref_no.observeEventType(.Value, withBlock: {
//            snapshot in
//            println("\(snapshot.key) -> \(snapshot.value)")
//        })
                    //user1_choices_array = [
            
            
            
            
            
            
            
        return true
    }

    func applicationWillResignActive(application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }


}













