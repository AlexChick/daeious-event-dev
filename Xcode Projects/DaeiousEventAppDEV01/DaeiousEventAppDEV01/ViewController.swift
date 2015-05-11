//
//  ViewController.swift
//  DaeiousEventAppDEV01
//
//  Created by Alexander Warren Chick on 5/10/15.
//  Copyright (c) 2015 Daeious.com. All rights reserved.
//

import UIKit
import Parse

class ViewController: UIViewController {
    
    
    @IBAction func changeText(sender: UIButton) {
        customTextLabel.text = "...changes this text."
    }
    
    @IBAction func queryParseForObjects(sender: UIButton) {
        var query = PFQuery(className:"zE0001R1")
        query.whereKey("m_ipadNum", equalTo: 24)
        query.orderByAscending("ixNum")
        query.findObjectsInBackgroundWithBlock {
            (objects: [AnyObject]?, error: NSError?) -> Void in
            
            if error == nil {
                // The find succeeded.
                println("Successfully retrieved \(objects!.count) interaction objects.")
                // Do something with the found objects
                if let objects = objects as? [PFObject] {
                    for object in objects {
                        println(object.objectId)
                    }
                    let m_userNum : String = String(stringInterpolationSegment: objects[1]["m_userNum"]!)
                    self.m_userNum_label.text = m_userNum
                    self.f_userNum_label.text = String(stringInterpolationSegment: objects[1]["f_userNum"]!)
                    println(objects[1]["m_userNum"]!)
                    println(objects[1])
                    
                }
            } else {
                // Log details of the failure
                println("Error: \(error!) \(error!.userInfo!)")
            }
        }
        
    }
    
    @IBOutlet var m_userNum_label: UILabel!
    @IBOutlet var f_userNum_label: UILabel!
    
    @IBOutlet var customTextLabel: UILabel!
    
    @IBOutlet var interactionsTableViewController: UITableView!
    
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        var query = PFQuery(className:"zE0001R1")
        query.whereKey("m_ipadNum", equalTo: 24)
        query.orderByAscending("ixNum")
        query.findObjectsInBackgroundWithBlock {
            (objects: [AnyObject]?, error: NSError?) -> Void in
            
            if error == nil {
                // The find succeeded.
                println("Successfully retrieved \(objects!.count) interaction objects.")
                // Do something with the found objects
                if let objects = objects as? [PFObject] {
                    for object in objects {
                        println(object.objectId)
                    }
                    let m_userNum : String = String(stringInterpolationSegment: objects[1]["m_userNum"]!)
                    self.m_userNum_label.text = m_userNum
                    self.f_userNum_label.text = String(stringInterpolationSegment: objects[1]["f_userNum"]!)
                    println(objects[1])
                    
                }
            } else {
                // Log details of the failure
                println("Error: \(error!) \(error!.userInfo!)")
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

