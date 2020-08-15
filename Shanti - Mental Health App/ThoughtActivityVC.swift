//
//  WhatWentWrongVC.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/26/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class WhatWentWrongVC: UIViewController {

    
    @IBOutlet weak var mainView: UIView!
    @IBOutlet weak var input1: UITextField!
    @IBOutlet weak var input2: UITextField!
    @IBOutlet weak var input3: UITextField!
    @IBOutlet weak var input4: UITextField!
    @IBOutlet weak var input5: UITextField!
    
    var url = String(format: "")
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = view.bounds
        gradientLayer.colors = [#colorLiteral(red: 0.9686274529, green: 0.78039217, blue: 0.3450980484, alpha: 1).cgColor, #colorLiteral(red: 0.8549019694, green: 0.250980407, blue: 0.4784313738, alpha: 1).cgColor]
        gradientLayer.shouldRasterize = true
        mainView.layer.addSublayer(gradientLayer)
        
        var shouldAutorotate: Bool {
            return false
        }
    
        
        // Do any additional setup after loading the view.
    }
    
    @IBAction func nextBtn(_ sender: Any) {
        if input1.text!.isEmpty {
            input1.text = ""
        }
        
        if input2.text!.isEmpty {
            input2.text = ""
        }
        
        if input3.text!.isEmpty {
            input3.text = ""
        }

        if input4.text!.isEmpty {
            input4.text = ""
        }

        if input5.text!.isEmpty {
            input5.text = ""
        }


        let Url = url
        guard let serviceUrl = URL(string: Url) else { return }
        let parameterDictionary = [
            "input1":input1.text!,
            "input2":input2.text!,
            "input3":input3.text!,
            "input4":input4.text!,
            "input5":input5.text!,
        ]
        var request = URLRequest(url: serviceUrl)
        request.httpMethod = "POST"
        request.setValue("Application/json", forHTTPHeaderField: "Content-Type")
        guard let httpBody = try? JSONSerialization.data(withJSONObject: parameterDictionary, options: []) else { return }
                request.httpBody = httpBody

                let session = URLSession.shared
                session.dataTask(with: request) { (data, response, error) in
                if let response = response {
                    print(response)
                }
                if let data = data {
                    let json = String(data: data, encoding: .utf8)!
                    print(json)
                }
                       
                }.resume()
        
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
