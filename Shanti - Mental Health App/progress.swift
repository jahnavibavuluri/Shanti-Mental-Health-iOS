//
//  progress.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/20/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

@IBDesignable
class progress: UIView {

    
        @IBInspectable var color: UIColor? = .lightGray
        var progress: CGFloat = 0.5
        
        override func draw(_ rect: CGRect) {
            let backgroundMask = CAShapeLayer()
            backgroundMask.path = UIBezierPath(roundedRect: rect, cornerRadius: rect.height*0.25).cgPath
            //backgroundMask.strokeColor = UIColor.lightGray.cgColor
            //backgroundMask.lineWidth = 20
            //backgroundMask.lineCap = CAShapeLayerLineCap.round
            layer.mask = backgroundMask
            
            let pBar = CGRect(origin: .zero, size: CGSize(width: rect.width*progress,height:rect.height))
            let pBarLayer = CALayer()
            pBarLayer.frame = pBar
        
            layer.addSublayer(pBarLayer)
            pBarLayer.backgroundColor = UIColor.darkGray.cgColor
        }

}
