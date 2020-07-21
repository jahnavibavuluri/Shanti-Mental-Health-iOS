//
//  SignupViewController.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/18/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class SignupViewController: UIViewController {

    @IBOutlet weak var usernameField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var emailField: UITextField!
    
    @IBOutlet weak var mainView: UIView!
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
        
    }
    
    @IBAction func signupButton(_ sender: Any) {
        let Url = String(format: "http://127.0.0.1:5000/signup")
        guard let serviceUrl = URL(string: Url) else { return }
        let parameterDictionary = ["username" : usernameField.text!, "password" : passwordField.text!, "email": emailField.text!]
        var request = URLRequest(url: serviceUrl)
        request.httpMethod = "POST"
        request.setValue("Application/json", forHTTPHeaderField: "Content-Type")
        guard let httpBody = try? JSONSerialization.data(withJSONObject: parameterDictionary, options: []) else {
                return
            }
        request.httpBody = httpBody

        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let response = response {
                print(response)
            }
            if let data = data {
            let json = String(data: data, encoding: .utf8)!
                print(json)
                if (json=="user or email exists") {
                    OperationQueue.main.addOperation {
                        let alert = UIAlertController(title: "Oops!", message: "Looks like that email or username already exists!", preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                        self.present(alert, animated: true)
                    }
                } else {
                    OperationQueue.main.addOperation {
                        self.performSegue(withIdentifier: "signinWelcome", sender: self)
                    }
                }
            }
        }.resume()
    }
    
    
    @IBAction func backtoLogin(_ sender: Any) {
        performSegue(withIdentifier: "backtoLogin", sender: self)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "signinWelcome" {
            var vc = segue.destination as! RecentstatViewController
        }
        if segue.identifier == "backtoLogin" {
            var vc = segue.destination as! ViewController
        }
    }
    
    }
    

