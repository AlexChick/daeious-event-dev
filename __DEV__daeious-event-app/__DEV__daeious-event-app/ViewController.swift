//
//  ViewController.swift
//  __DEV__daeious-event-app
//
//  Created by Alexander Warren Chick on 4/23/15.
//  Copyright (c) 2015 The Intro Game LLC. All rights reserved.
//

import UIKit

let DaeiousFirebaseURL = "https://burning-fire-8681.firebaseio.com"

class ViewController: UIViewController {

        
    
    
    @IBOutlet var no_count_label: UILabel!
    @IBOutlet var mn_count_label: UILabel!
    @IBOutlet var my_count_label: UILabel!
    @IBOutlet var yes_count_label: UILabel!
    
    
    @IBAction func no_button_tapped(sender: UIButton) {
        var count = no_count_label.text!.toInt()!
        count += 1
        no_count_label.text = "\(count)"
    }
    @IBAction func mn_button_tapped(sender: UIButton) {
    }
    @IBAction func my_button_tapped(sender: UIButton) {
    }
    @IBAction func yes_button_tapped(sender: UIButton) {
    }
    
    
    
    
    
    
    
    
    
    
//    @IBAction func see_again_button(sender: UIButton) {
//        if sender.titleLabel == "No" {
//            var no_count: String = see_again_count_no.text!
//            see_again_count_no.text = "\(no_count.toInt()! + 1)"
//        }
//        var currentLabel = sender.titleLabel!.text!.toInt()
//        println(currentLabel)
//        println(sender.titleLabel)
//        
//        
//    }
    
    @IBAction func randomize(sender: UIButton) {
        no_count_label.text = "\(arc4random_uniform(21))"
        mn_count_label.text = "\(arc4random_uniform(21))"
        my_count_label.text = "\(arc4random_uniform(21))"
        yes_count_label.text = "\(arc4random_uniform(21))"
    }
    
    @IBAction func reset_to_zero(sender: UIButton) {
        no_count_label.text = "\(0)"
        mn_count_label.text = "\(0)"
        my_count_label.text = "\(0)"
        yes_count_label.text = "\(0)"
    }
    
    
    
    func getFirebaseData() {
        
        
    }
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        getFirebaseData()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    


}

