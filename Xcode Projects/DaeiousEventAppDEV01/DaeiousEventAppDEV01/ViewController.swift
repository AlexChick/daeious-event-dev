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
    

// Constants
    
    
// Variables
    
    var thisEventNum: Int?
    
    var li_Objects_R1_Ix: [AnyObject]?
    
    var myR1QueryTimer: NSTimer = NSTimer()
    
    
// Labels
    
    @IBOutlet var m_userNum_label: UILabel!
    @IBOutlet var f_userNum_label: UILabel!
    @IBOutlet var customTextLabel: UILabel!
    
    
// Buttons
    
    @IBAction func changeText(sender: UIButton) {
        customTextLabel.text = "...changes this text."
    }
    
    @IBAction func queryParseForObjects(sender: UIButton) {
        fetch_IxObjectsFromParse()
    }

// Functions
    
    func fetch_IxObjectsFromParse() {
        var query = PFQuery(className:"zE0001R1")
        query.whereKey("m_ipadNum", equalTo: 1)
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
                    println(objects[7])
                }
            } else {
                // Log details of the failure
                println("Error: \(error!) \(error!.userInfo!)")
            }
        }
    }
    
//    func fetch_SingleObjectFromParse(classToQuery: String, keyToQuery: String, valueToQuery: Int) -> PFObject {
//        var query = PFQuery(className: classToQuery)
//        query.whereKey(keyToQuery, equalTo: valueToQuery)
//        query.get
//        query.findObjectsInBackgroundWithBlock {
//            (objects: [AnyObject]?, error: NSError?) -> AnyObject! in
//            
//            if error == nil {
//                if let objects = objects as? [PFObject] {
//                    if let returningObject = objects[0] as? PFObject {
//                        return returningObject
//                    }
//                }
//            }
//            else {
//                println("Error: \(error!) \(error!.userInfo!)")
//                return
//            }
//        } // end query
//    } // end function
    
    func fetch_ConfigObjectFromParse() {
        var query = PFQuery(className: "Config")
        query.whereKey("eventNum", equalTo: 1)
        query.findObjectsInBackgroundWithBlock { (objects: [AnyObject]?, error: NSError?) -> Void in
            if error == nil {
                // The find succeeded.
                if let objects = objects as? [PFObject] {
                    if let queryable = objects[0]["canQueryForR1"] as? Bool {
                        if queryable {
                            println("Yes! The R1 interaction objects are ready to be queried.")
                            self.myR1QueryTimer.invalidate()
                            self.fetch_IxObjectsFromParse()
                        }
                        else {
                            println("No! The R1 interaction objects aren't ready yet!")
                        }
                    }
                }
            }
            else {
                // The find failed.
                println("Error: \(error!) \(error!.userInfo!)")
            }
        }
    }
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        myR1QueryTimer = NSTimer.scheduledTimerWithTimeInterval(5,
                                target: self,
                                selector: Selector("fetch_ConfigObjectFromParse"),
                                userInfo: nil,
                                repeats: true)
        
        //self.fetch_IxObjectsFromParse()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

