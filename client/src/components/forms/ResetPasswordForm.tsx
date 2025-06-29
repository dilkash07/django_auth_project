import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  resetPasswordFormValues,
  resetPasswordSchema,
} from "@/schemas/resetPassword.schema";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { useState } from "react";
import { ArrowLeft, Eye, EyeOff } from "lucide-react";
import { Link } from "react-router-dom";
import { MdLockReset } from "react-icons/md";

const ResetPasswordForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const form = useForm<resetPasswordFormValues>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      password: "",
      confirmPassword: "",
    },
  });

  const onsubmit = (data: resetPasswordFormValues) => {
    console.log("Form Data: ", data);
  };
  return (
    <div className="max-w-md mx-auto p-6 rounded-2xl shadow-md bg-white dark:bg-zinc-900">
      <div className="flex flex-col gap-2 items-center mb-6">
        <MdLockReset size={56} />
        <h1 className="text-3xl font-serif italic font-semibold mb-4 text-center">
          Reset Your Passwrod?
        </h1>
        <p className="text-sm italic text-center">
          We’re here to assist you in regaining access to your account. Please
          follow the steps outlined below to reset your password and get back to
          using our services seamlessly.
        </p>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onsubmit)} className="space-y-2">
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="********"
                      {...field}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword((prev) => !prev)}
                      className="absolute right-2 top-2 text-muted-foreground"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="confirmPassword"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Confirm Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <Input
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="********"
                      {...field}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword((prev) => !prev)}
                      className="absolute right-2 top-2 text-muted-foreground"
                    >
                      {showConfirmPassword ? (
                        <EyeOff size={18} />
                      ) : (
                        <Eye size={18} />
                      )}
                    </button>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="pt-4">
            <Button type="submit" className="w-full">
              Submit
            </Button>
          </div>
        </form>
      </Form>

      <div className="mt-4">
        <Link
          to={"/login"}
          className="flex gap-1 items-center justify-center hover:underline"
        >
          <ArrowLeft size={18} /> Back to Login
        </Link>
      </div>
    </div>
  );
};

export default ResetPasswordForm;
