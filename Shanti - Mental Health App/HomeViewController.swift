//
//  HomeViewController.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/18/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class HomeViewController: UIViewController {
    
    
    @IBOutlet weak var firstnameField: UITextField!
    @IBOutlet weak var lastnameField: UITextField!
    @IBOutlet weak var ageField: UITextField!
    
    @IBOutlet weak var femaleField: UIImageView!
    @IBOutlet weak var maleField: UIImageView!
    @IBOutlet weak var otherField: UIImageView!
    
    
    @IBOutlet weak var reading: UIImageView!
    @IBOutlet weak var gardening: UIImageView!
    @IBOutlet weak var cooking: UIImageView!
    @IBOutlet weak var dancing: UIImageView!
    @IBOutlet weak var traveling: UIImageView!
    @IBOutlet weak var watchingTV: UIImageView!
    @IBOutlet weak var videogames: UIImageView!
    @IBOutlet weak var exercise: UIImageView!
    @IBOutlet weak var shopping: UIImageView!
    @IBOutlet weak var singing: UIImageView!
    
    @IBOutlet weak var sports: UIImageView!
    @IBOutlet weak var art: UIImageView!
    @IBOutlet weak var food: UIImageView!
    @IBOutlet weak var health: UIImageView!
    @IBOutlet weak var technology: UIImageView!
    @IBOutlet weak var animals: UIImageView!
    @IBOutlet weak var socialmedia: UIImageView!
    @IBOutlet weak var music: UIImageView!
    @IBOutlet weak var outdoors: UIImageView!
    @IBOutlet weak var popculture: UIImageView!
    
    @IBOutlet weak var family: UIImageView!
    @IBOutlet weak var friends: UIImageView!
    @IBOutlet weak var significantother: UIImageView!
    @IBOutlet weak var spiritualleader: UIImageView!
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(HomeViewController.imageTapped(gesture:)))
        maleField.addGestureRecognizer(tapGesture)
        maleField.isUserInteractionEnabled = true
        
        
       
        // Do any additional setup after loading the view.
    }
    
    @objc func imageTapped(gesture: UIGestureRecognizer) {
        print("tapped!")
    }
    
    @IBAction func nextButton(_ sender: Any) {
            }
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}


