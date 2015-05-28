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
    
    var thisEventNum = Int()
    
    var counter_IndexOfIxInList: Int = 0
    
    var li_Objects_R1_Ix = [PFObject]()
    
    var myR1QueryTimer: NSTimer = NSTimer()
    var timer_Ix: NSTimer = NSTimer()
    

    
    
// Labels
    
    // view_topBar
    @IBOutlet var label_yourName: UILabel!
    @IBOutlet var label_theirName: UILabel!
    @IBOutlet var label_timeRemaining: UILabel!
    @IBOutlet var label_round: UILabel!
    @IBOutlet var label_ix: UILabel!
    
    // view_questionAndAnswer
    @IBOutlet var label_question: UILabel!
    
    // view_devData
    @IBOutlet var label_m_userNum: UILabel!
    @IBOutlet var label_f_userNum: UILabel!
    @IBOutlet var label_m_iPadNum: UILabel!
    @IBOutlet var label_f_iPadNum: UILabel!
    @IBOutlet var label_ixNum: UILabel!
    
    // other
    @IBOutlet var label_ipadNum: UILabel!
    
    
    
// Buttons
    
    @IBAction func queryParseForObjects(sender: UIButton) {
        fetch_IxObjectsFromParse()
    }
    
    @IBAction func buttonPressed_NextInteraction(sender: AnyObject) {
    }

    
// Segmented Controls
    
    @IBAction func segmentedControlPressed_Answer(sender: AnyObject) {
    }
    
    @IBAction func segmentedControlPressed_SeeAgainChoice(sender: AnyObject) {
    }
    


/////////    END DECLARACTIONS    //////////
    
    
    
    
////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  Functions
//
////////////////////////////////////////////////////////////////////////////////////////////////////

    func fetch_EventObjectFromParse(eventNum: Int) {
        var query = PFQuery(className: "Event")
        query.whereKey("eventNum", equalTo: eventNum)
        // How do I retrieve just one object with a query asynchronously?
    }
    
    func reload_Ix() {
        // This is called inside timer_Ix when the previous interaction ends and a new one begins,
        // after the list of ix objects has been retrieved.
        // All relevant values are displayed to the User.
        
        if self.counter_IndexOfIxInList < self.li_Objects_R1_Ix.count {
        
            if let currentIx = self.li_Objects_R1_Ix[self.counter_IndexOfIxInList] as PFObject? {
                
                self.label_yourName.text = String(stringInterpolationSegment: currentIx["m_username"]!)
                self.label_theirName.text = String(stringInterpolationSegment: currentIx["f_username"]!)
                self.label_ix.text = String(stringInterpolationSegment: self.counter_IndexOfIxInList + 1) + " of \(self.li_Objects_R1_Ix.count)"
                self.label_ixNum.text = String(stringInterpolationSegment: currentIx["ixNum"]!)
                self.counter_IndexOfIxInList += 1
            }
                
            else {
                
                println("Something went wrong. End of interactions, maybe? Counter: \(self.counter_IndexOfIxInList)")
            }
        }
        
        else {
            self.timer_Ix.invalidate()
        }
        

        
        
    }
    
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
                        self.li_Objects_R1_Ix.append(object)
                    }
                    let m_userNum : String = String(stringInterpolationSegment: objects[1]["m_userNum"]!)
                    self.label_m_userNum.text = m_userNum
                    self.label_f_userNum.text = String(stringInterpolationSegment: objects[1]["f_userNum"]!)
                    println(objects[7])
                    
                    self.timer_Ix = NSTimer.scheduledTimerWithTimeInterval(
                        2,
                        target: self,
                        selector: Selector("reload_Ix"),
                        userInfo: nil,
                        repeats: true)
                    
                    
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
        
        myR1QueryTimer = NSTimer.scheduledTimerWithTimeInterval(
            5,
            target: self,
            selector: Selector("fetch_ConfigObjectFromParse"),
            userInfo: nil,
            repeats: true)
        
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

